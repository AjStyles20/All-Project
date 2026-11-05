"""Encryption at rest with Windows DPAPI (CryptProtectData), tied to the user's Windows account.

No key is stored by this program: Windows derives it from the user's logon credentials.
"""
import ctypes
import sys


class DPAPIProtector:
    def __init__(self):
        if sys.platform != "win32":
            raise RuntimeError("Windows DPAPI is only available on Windows.")
        from ctypes import wintypes

        class Blob(ctypes.Structure):
            _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

        self._Blob = Blob
        self._crypt32 = ctypes.windll.crypt32
        self._kernel32 = ctypes.windll.kernel32
        # Keep the entropy fixed per application so other DPAPI users' blobs do not open here.
        self._entropy = b"P009 screen memory v1"

    def _call(self, fn, data: bytes) -> bytes:
        source = self._Blob(len(data), ctypes.cast(ctypes.create_string_buffer(data, len(data)), ctypes.POINTER(ctypes.c_char)))
        entropy = self._Blob(len(self._entropy), ctypes.cast(ctypes.create_string_buffer(self._entropy, len(self._entropy)),
                                                              ctypes.POINTER(ctypes.c_char)))
        out = self._Blob()
        # CRYPTPROTECT_UI_FORBIDDEN = 0x1: never show a prompt.
        if not fn(ctypes.byref(source), None, ctypes.byref(entropy), None, None, 0x1, ctypes.byref(out)):
            raise OSError("DPAPI call failed")
        try:
            return ctypes.string_at(out.pbData, out.cbData)
        finally:
            self._kernel32.LocalFree(out.pbData)

    def protect(self, data: bytes) -> bytes:
        # Both functions take (in, description, entropy, reserved, prompt, flags, out).
        return self._call(self._crypt32.CryptProtectData, data)

    def unprotect(self, data: bytes) -> bytes:
        return self._call(self._crypt32.CryptUnprotectData, data)

"""Windows-only probes: foreground window, idle time, lock state, and window capture.

Only the foreground window's rectangle is captured (privacy model §2.3).
"""
import ctypes
import io
import os
from ctypes import wintypes

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
psapi = ctypes.windll.psapi

PROCESS_QUERY_LIMITED_INFORMATION = 0x1000


class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.UINT), ("dwTime", wintypes.DWORD)]


def foreground():
    """(program file name, title, (left, top, right, bottom)) or None when there is no window."""
    hwnd = user32.GetForegroundWindow()
    if not hwnd or user32.IsIconic(hwnd):
        return None
    length = user32.GetWindowTextLengthW(hwnd)
    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buffer, length + 1)
    pid = wintypes.DWORD()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    rect = wintypes.RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(rect))
    return _program(pid.value), buffer.value, (rect.left, rect.top, rect.right, rect.bottom)


def _program(pid: int) -> str:
    handle = kernel32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    if not handle:
        return "unknown"
    try:
        size = wintypes.DWORD(1024)
        buffer = ctypes.create_unicode_buffer(size.value)
        if kernel32.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(size)):
            return os.path.basename(buffer.value)
        return "unknown"
    finally:
        kernel32.CloseHandle(handle)


def seconds_since_input() -> float:
    info = LASTINPUTINFO(ctypes.sizeof(LASTINPUTINFO), 0)
    user32.GetLastInputInfo(ctypes.byref(info))
    return max(0, (kernel32.GetTickCount() - info.dwTime) & 0xFFFFFFFF) / 1000


def locked() -> bool:
    # While the lock screen (or a secure desktop such as UAC) is up, the input desktop
    # cannot be opened by a normal process.
    desktop = user32.OpenInputDesktop(0, False, 0x0100)  # DESKTOP_SWITCHDESKTOP
    if not desktop:
        return True
    user32.CloseDesktop(desktop)
    return False


def capture(rect):
    """Image of one screen rectangle, or None if it is empty or off-screen."""
    from PIL import ImageGrab
    left, top, right, bottom = rect
    if right - left < 16 or bottom - top < 16:
        return None
    try:
        return ImageGrab.grab(bbox=rect, all_screens=True)
    except OSError:
        return None


def signature(image) -> tuple:
    return tuple(image.convert("L").resize((16, 16)).getdata())


def encode(image, max_width=1600, quality=60) -> bytes:
    if image.width > max_width:
        image = image.resize((max_width, int(image.height * max_width / image.width)))
    out = io.BytesIO()
    image.convert("RGB").save(out, format="WEBP", quality=quality)
    return out.getvalue()


def dpi_aware():
    # Without this, window rectangles are scaled on high-DPI screens and the capture is cropped.
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except (AttributeError, OSError):
        user32.SetProcessDPIAware()

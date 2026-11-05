"""P002 educational language model laboratory."""
import os

# On small CPUs, multi-threaded BLAS fights itself over tiny matrices: one thread measured
# 3x faster on the development laptop. Must be set before NumPy is first imported.
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")

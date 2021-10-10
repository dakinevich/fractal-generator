from numba import njit, prange


@njit(parallel = True, fastmath = True)
def f(x):
    for i in prange(x):
        pass
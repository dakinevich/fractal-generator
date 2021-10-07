from math import sqrt
import numpy as np
import ctypes
import time
import matplotlib.pyplot as plt

try:
    w, h = ctypes.windll.user32.GetSystemMetrics(0),\
           ctypes.windll.user32.GetSystemMetrics(1)
except AttributeError:
    w, h = 1536, 864

center_ind = [(w-1)/2,(h-1)/2]

t = time.time()
arr =[[0 for _ in range(w)] for _ in range(h)]
for ix in range(w):
    for iy in range(h):
        arr[iy][ix] = sqrt((w/2 - ix)**2+(h/2-iy)**2)
print(time.time()-t)
#print(sum(arr[j][i] for i in range(w) for j in range(h)))

t = time.time()
arr = np.ndarray((w, h), np.float64)
for ix in range(w):
    arr[ix, :] = np.sqrt((w/2 - ix)**2+(h/2-np.arange(h))**2)
print(time.time()-t)

t = time.time()
arr = np.sqrt(np.full((w,h),np.array(np.arange(h)-center_ind[1],np.float64)**2) + np.transpose(np.full((h,w),np.array(np.arange(w)-center_ind[0],np.float64)**2)))
print(time.time()-t)

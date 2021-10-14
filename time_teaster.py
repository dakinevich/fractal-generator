import numpy as np
from PIL import Image, ImageDraw
from time import time as ti
from numba import njit, prange
from matplotlib import pyplot as pt
import sys

@njit
def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < iter:
        z = z*z + c  # fractal formula (z = z*z + c)
        n += 1
    return n

@njit
def render(arr,w, h):
    np_img = np.zeros(arr.shape, dtype=np.int8)
    for ix in prange(w):  # main time-eater
        for iy in prange(h):
            c = arr[ix, iy]
            m = mandelbrot(c)
            #chennel = 255 - int(m * 255 / iter)
            np_img[ix, iy] = m
    #chennel = 255 - int(m * 255 / iter)
    return np_img



'''flatten
@njit
def render(arr, w, h):
    arr.flatten()
    np_img = np.zeros(arr.shape, dtype=np.int8)
    for coord in range(w*h):  # main time-eater
        ix = coord % w
        iy = coord // w
        c = arr[ix, iy]
        m = mandelbrot(c)
        #chennel = 255 - int(m * 255 / iter)
        np_img[ix, iy] = m
    #chennel = 255 - int(m * 255 / iter)
    return np_img
'''

def inter(l, times=1):
    for _ in range(times):
        for i in range(1, len(l)-1):
            l[i] = (l[i-1] + l[i+1] + l[i])/3
    return l


if __name__ == "__main__":
    # pygame.init()
    t = ti()
    w, h = 1920, 1080
    '''screen = pygame.display.set_mode((w,h))

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()'''

    move_x = 0
    move_y = 0
    zoom = 1
    iter = 20

    main_set = np.zeros((w, h), complex)

    real_axis = np.array((np.arange(w),), dtype=np.float64)  # gradient
    imag_axis = np.array((np.arange(h),), dtype=np.float64)

    real_axis += -(w-1)/2 + move_x  # bias
    imag_axis += -(h-1)/2 + move_y

    real_axis /= (h-1)/4 * zoom  # zoom
    imag_axis /= (h-1)/4 * zoom

    real_axis = (real_axis*complex(1)).transpose()  # layering real and imag
    imag_axis = imag_axis*complex(1j)
    main_set += real_axis + imag_axis

    time_data = []

    print('pre_culc', ti() - t, '\n')

    ticks = 200
    t10 = int(ticks/10 + 0.5)
    t100 = int(ticks/100 + 0.5)

    for tick in range(ticks):
        if tick == t10:
            print('10%')
        elif tick == t100:
            print('1%')
        t = ti()
        res = render(main_set, w, h)  # sdl
        im = Image.fromarray(res.transpose())
        #im.show()
        time_data.append(ti() - t)

    print('data collected')
    #time_data = time_data[1:-1]
    # pygame.display.flip()
    pt.plot(list(range(len(time_data))), time_data)
    print('first plot')
    time_data = inter(time_data, 20)
    print('interpolation')
    pt.plot(list(range(len(time_data))), time_data)
    print('second plot')
    pt.show()

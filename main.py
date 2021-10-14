import time
import numpy as np
from PIL import Image, ImageDraw
from numba import njit, prange
from matplotlib import pyplot as pt


@njit(fastmath=True)
def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < iter:
        z = z*z + c  # fractal formula (z = z*z + c)
        n += 1
    return n


@njit(parallel=True, fastmath=True)
def render(arr):
    np_img = np.zeros(arr.shape, dtype=np.int32)
    for coord in prange(w*h):  # main time-eater
        ix = coord % w
        iy = coord // w
        c = arr[ix, iy]
        m = mandelbrot(c)
        np_img[ix, iy] = m
    return np_img


@njit(fastmath=True)
def main_set_mapping(real_axis_in, imag_axis_in, main_set_in, move_x_in, move_y_in, zoom_in):
    # bias
    real_axis_in += -(w-1)/2 + move_x_in  
    imag_axis_in += -(h-1)/2 + move_y_in
    # zoom
    real_axis_in /= (h-1)/4 * zoom_in  
    imag_axis_in /= (h-1)/4 * zoom_in
    # layering real and imag
    real_axis_in = (real_axis_in*complex(1)).transpose()
    imag_axis_in = imag_axis_in*complex(1j)
    main_set_in += real_axis_in + imag_axis_in

    return main_set_in


if __name__ == "__main__":
    # pygame.init()

    # init
    w, h = 1920, 1080

    move_x = 0
    move_y = 0
    zoom = 1
    iter = 100

    main_set = np.zeros((w, h), complex)
    # gradient
    real_axis = np.array((np.arange(w),), dtype=np.float64)  
    imag_axis = np.array((np.arange(h),), dtype=np.float64)
    '''
    screen = pygame.display.set_mode((w,h))
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
    '''
    main_set = main_set_mapping(real_axis, imag_axis, main_set, move_x, move_y, zoom)
    res = render(main_set)  # pre-render cashing

    t = time.time()

    res = render(main_set)  # sdl
    res = 255 - res*255/iter
    im = Image.fromarray(res.transpose())
    
    print(time.time()-t)

    im.show()


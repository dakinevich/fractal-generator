import numpy as np
from PIL import Image, ImageDraw

def mandelbrot(c):
    z, n = 0, 0
    while abs(z) <= 2 and n < iter:
        z = z*z + c
        n += 1
    return n

def render(arr):
    im = Image.new('RGB', (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    for ix in range(w):
        for iy in range(h):
            c = arr[ix, iy]
            m = mandelbrot(c)
            chennel = 255 - int(m * 255 / iter)
            draw.point([ix, iy], (chennel, chennel, chennel))
    im.save('output.png', 'PNG')

w, h = 1920, 1080
iter = 20
main_set = np.zeros((w, h), np.complex)

real_axis = np.array((np.arange(w),), dtype=np.float64)-(w-1)/2
imag_axis = np.array((np.arange(h),), dtype=np.float64)-(h-1)/2

real_axis /= (h-1)/4
imag_axis /= (h-1)/4

main_set += (real_axis*complex(1)).transpose() + imag_axis*complex(1j)

render(main_set)

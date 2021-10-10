import numpy as np
from PIL import Image, ImageDraw


def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < iter:
        z = z*z + c  # fractal formula (z = z*z + c)
        n += 1
    return n


def render(arr):
    im = Image.new('RGB', (w, h), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    for ix in range(w):  # main time-eater
        for iy in range(h):
            c = arr[ix, iy]
            m = mandelbrot(c)
            chennel = 255 - int(m * 255 / iter)
            draw.point([ix, iy], (chennel, chennel, chennel))
    im.save('output.png', 'PNG')


if __name__ == "__main__":
    w, h = 1920, 1080
    move_x = 0
    move_y = 0
    zoom = 1
    iter = 20

    main_set = np.zeros((w, h), np.complex)

    real_axis = np.array((np.arange(w),), dtype=np.float64)  # gradient
    imag_axis = np.array((np.arange(h),), dtype=np.float64)

    real_axis += -(w-1)/2 + move_x  # bias
    imag_axis += -(h-1)/2 + move_y

    real_axis /= (h-1)/4 * zoom  # zoom
    imag_axis /= (h-1)/4 * zoom

    real_axis = (real_axis*complex(1)).transpose()  # layering real and imag
    imag_axis = imag_axis*complex(1j)
    main_set += real_axis + imag_axis

    render(main_set)

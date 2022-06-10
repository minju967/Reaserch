import pyvista as pv
from pyvista import examples
import numpy as np
mesh = pv.read('C:\\Users\\user\\PycharmProjects\\Reaserch\\data_sample\\obj\\A_class.obj')
x_min, x_max, y_min, y_max, z_min, z_max = mesh.bounds
x_length = x_max - x_min
y_length = y_max - y_min
z_length = z_max - z_min

print(round(x_length, 3), round(y_length, 3), round(z_length, 3))

def show():
    # axis = 'y' --> cpos = 'zx'
    slices = mesh.slice_along_axis(n=20, axis='y')
    # slices.plot(line_width=2)

    for name in slices.keys():
        block = slices[name]
        block.plot(line_width=2, cpos='zx', background='black')

    # axis = 'z' --> cpos = 'yx'
    slices = mesh.slice_along_axis(n=20, axis='z')
    # slices.plot(line_width=2)

    for name in slices.keys():
        block = slices[name]
        block.plot(line_width=2, cpos='yx', background='black')
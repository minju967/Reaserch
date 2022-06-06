import pyvista as pv


path = 'C:\\Users\\MINJU\\PycharmProjects\\Coding_test\\Reaserch\\data_sample\\obj\\sample1.obj'
mesh1 = pv.read(path)
print(mesh1)
pl = pv.Plotter(shape=(1, 2))
pl.subplot(0, 0)
pl.show_axes()
# pl.set_background('white')
_ = pl.show_grid()
_ = pl.add_mesh(mesh1)
pl.camera_position = (0.0, 1.0, 0.0)
mesh1.save('sample1.stl')

pl.subplot(0, 1)
pl.show_axes()
# pl.set_background('white')
_ = pl.show_grid()
mesh2 = mesh1.scale([10.0,10.0,10.0], transform_all_input_vectors=True, inplace=True)
mesh2.save('scale_mesh.stl')
print(mesh2)
_ = pl.add_mesh(mesh2)
pl.camera_position = (0.0, 1.0, 0.0)

# pl.show()

# import pyvista as pv
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
# from pyvista import examples

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def z_rotate(mesh, plotter, i, path, angle):
    mesh.rotate_z(i)
    plotter.camera_position = (0.0, 1.0, 0.0)
    plotter.camera.elevation = angle
    plotter.show(screenshot=path, window_size=(2000,2000))
    plotter.close()

def y_rotate(mesh, plotter, i, path, angle):
    mesh.rotate_z(90)
    mesh.rotate_y(i)
    plotter.camera_position = (1.0, 0.0, 0.0)
    plotter.camera.azimuth = angle
    plotter.show(screenshot=path, window_size=(2000,2000))
    plotter.close()

def adjust_position(mesh, plotter, z, y, img_path, y_rot, x_rot):
    # cpos = [(0.2, 0.3, 0.9), (0, 0, 0), (0, 1, 0)]
    if y != 0:
        mesh.rotate_z(90)
    mesh.rotate_z(z)
    mesh.rotate_y(y)
    plotter.camera_position = (1.0, 0.0, 0.0)
    plotter.camera.elevation = y_rot
    plotter.camera.azimuth = x_rot
    plotter.camera.zoom(0.8)
    plotter.screenshot(img_path, window_size = (2000,2000))
    plotter.close()


# 6view 생성
def create_6View(cls_obj_path, screen_img, obj_name):
    path = os.path.join(cls_obj_path, obj_name)
    cnt = 0
    image_pathes = []

    for i in range(4):
        mesh = pv.read(path)
        plotter = pv.Plotter(off_screen=True)
        plotter.set_background('white')
        actor = plotter.add_mesh(mesh)
        # plotter.camera_position = (1.0, 0.0, 0.0)

        img_path = os.path.join(screen_img, obj_name.replace('.obj','_')+str(cnt)+'.png')
        z_rotate(mesh, plotter, i*90, img_path, 0)
        cnt += 1
        image_pathes.append(img_path)

    for i in range(0,4,2):
        mesh = pv.read(path)
        plotter = pv.Plotter(off_screen=True)
        plotter.set_background('white')
        actor = plotter.add_mesh(mesh)
        # plotter.camera_position = (1.0, 0.0, 0.0)

        img_path = os.path.join(screen_img, obj_name.replace('.obj','_')+str(cnt)+'.png')
        y_rotate(mesh, plotter, (i*90)+90, img_path, 0)
        cnt += 1
        image_pathes.append(img_path)

    return image_pathes

def create_Nview(obj_name, cls_obj_path, screen_img, heat_map, rotate, count):
    max_value = max(np.max(heat_map, axis=1))
    re_index = np.where(heat_map>max_value*0.5)
    cnt = count
    view_list = []
    rot_list = [[0,0], [90,0], [180,0], [270,0], [0,90], [0,270]]
    for y_idx,x_idx in zip(re_index[0], re_index[1]):
        y = y_idx * 40
        x = x_idx * 40

        path = os.path.join(cls_obj_path, obj_name)
        mesh = pv.read(path)
        plotter = pv.Plotter(off_screen=True)
        plotter.set_background('white')
        actor = plotter.add_mesh(mesh, reset_camera=True)
        plotter.set_focus(mesh.center)
        plotter.camera_set = False
        # plotter.camera_position = (1.0, 0.0, 0.0)
        img_path = os.path.join(screen_img, obj_name.replace('.obj','_view_')+str(cnt)+'.png')

        if y > 1000:
            y_angle = -(((y - 1000)/1000)*30)
        else:
            y_angle = 30 - ((y/1000)*30)

        y_angle = round(y_angle, 2)

        if x > 1000:
            x_angle = ((x - 1000)/1000)/30
        else:
            angle = (x/1000)*30
            x_angle = -(30 - angle)

        x_angle = round(x_angle, 2)

        Z = rot_list[rotate][0]
        Y = rot_list[rotate][1]
        print(Z, Y, y_angle, x_angle)
        adjust_position(mesh, plotter, Z, Y, img_path, y_angle, x_angle)
        cnt += 1
        view_list.append(img_path)
    return view_list


def create_heatmap(orb_image):
    src = cv2.imread(orb_image)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    target = cv2.imread(orb_image, cv2.IMREAD_GRAYSCALE)

    orb = cv2.ORB_create(
        nfeatures=40000,
        scaleFactor=1.2,
        nlevels=8,
        edgeThreshold=31,
        firstLevel=0,
        WTA_K=2,
        scoreType=cv2.ORB_HARRIS_SCORE,
        patchSize=31,
        fastThreshold=20,
    )

    kp1, des1 = orb.detectAndCompute(gray, None)
    kp2, des2 = orb.detectAndCompute(target, None)

    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)

    heatmap = np.zeros((50,50))
    for i in matches[:100]:
        idx = i.queryIdx
        x1, y1 = kp1[idx].pt
        heatmap[int(y1)//40][int(x1)//40] += 1

    return heatmap

def create_crop(crop_dir, img_path, cnt):
    crop_cnt = 0
    view_heatmap = create_heatmap(img_path)
    max_value = max(np.max(view_heatmap, axis=1))
    re_index = np.where(view_heatmap > max_value * 0.5)
    crop_size = 300
    _pass = False
    for y_idx, x_idx in zip(re_index[0], re_index[1]):
        if _pass == True:
            continue

        if y_idx < 8 or not _pass:
            y_idx = 8
            _pass = True

        if x_idx < 8 or not _pass:
            x_idx = 8
            _pass = True

        y = y_idx * 40
        x = x_idx * 40

        min_y = y - (crop_size // 2)
        max_y = y + (crop_size // 2)

        min_x = x - (crop_size // 2)
        max_x = x + (crop_size // 2)

        crop_path = os.path.join(crop_dir, str(cnt)+str(crop_cnt)+str(cnt)+'.png')
        while os.path.isfile(crop_path):
            crop_path = os.path.join(crop_dir, str(cnt)+str(crop_cnt)+str(cnt+1)+'.png')

        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        crop_img = img[min_y:max_y, min_x:max_x]
        crop_img = cv2.resize(crop_img, dsize=(224, 224))
        cv2.imwrite(crop_path, crop_img)
        crop_cnt += 1

        print(crop_path)
        print()


# obj_path = '/media/minju/CCF89352F8933A22/project/experiment7/Image_Crop/test'

# classes = ['A_train', 'B_train', 'C_train', 'D_train', 'E_train']
classes = ['A_test']
root_path = '/root/MINJU/data'
obj_path = '/media/minju/CCF89352F8933A22/project/data_alignment'

# classes = ['A']
# root_path = '/media/minju/CCF89352F8933A22/Crop_dataset'
# obj_path = '/media/minju/CCF89352F8933A22/project/data_alignment/KCC_OBJ'

# screen_img = '/media/minju/CCF89352F8933A22/project/experiment7/Image_Crop/test/A/V_Image'
# crop_dir = '/media/minju/CCF89352F8933A22/project/experiment7/Image_Crop/test/A/C_Image'
# orb_image = '/media/minju/CCF89352F8933A22/project/experiment7/Image_Crop/test/V_Image/154 bq_0.png'
# nview_image = '/media/minju/CCF89352F8933A22/project/experiment7/Image_Crop/test/A/V_Image/10311-343-153_view_0.png'
# obj_name = '154 bq.obj'


def main1():
    # view_list = create_6View('10311-343-153.obj')
    # heat_map = create_heatmap(view_list[0])
    # Nview_list = create_Nview('10311-343-153.obj', heat_map)

    for cls in classes:
        cls_obj_path = os.path.join(obj_path, cls)
        screen_img = os.path.join(root_path, cls, 'V_Image_view20')
        createFolder(screen_img)
        crop_dir = os.path.join(root_path, cls, 'C_Image_view20')
        createFolder(crop_dir)
        obj_list = os.listdir(cls_obj_path)
        cnt = 0
        for obj in obj_list:
            total_crop = 0
            view_list = create_6View(cls_obj_path, screen_img, obj)
            # view 생성 완 료
            for i, orb_image in enumerate(view_list):
                print(orb_image)
                heat_map = create_heatmap(orb_image)
                Nview_list = create_Nview(obj, cls_obj_path, screen_img, heat_map, i, cnt)
                cnt += len(Nview_list)
                crop_cnt = create_crop(crop_dir, obj, Nview_list)
                total_crop += crop_cnt



import time
import glob
import sys

if __name__ == "__main__":
    view20_path = '/root/MINJU/data/20view_dataset_562_2000'
    # classes = os.listdir(view20_path)
    classes = ['D']

    args = []
    for cls in classes:
        total_crop = 0
        crop_dir = os.path.join(root_path, 'view20_crop', cls)
        createFolder(crop_dir)
        cls_img_path = os.path.join(view20_path, cls)
        img_list =glob.glob(cls_img_path+'/*.png')

        for i, image in enumerate(img_list): 
            args.append([crop_dir, image, i])
        break


    start = time.time()

    p = multiprocessing.Pool(processes=90)
    proc = p.starmap(create_crop, args)

    print('run time: ', time.time()-start)

    p.close()

    p.join()


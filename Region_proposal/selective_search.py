import os.path

import selectivesearch
import cv2
import matplotlib.pyplot as plt
import pyvista as pv
import random
import time

random.seed(time)

def search_region(image, f):
    img = image
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    _, regions = selectivesearch.selective_search(img_rgb, scale=100, min_size=1000)
    cand_rects = [cand['rect'] for cand in regions]
    green_rgb = (125, 255, 51)

    for rect in cand_rects:
        # 테두리 제외
        print(rect)
        if rect[0] == 0 and rect[3] == 999:
            continue
        img_rgb_copy = img_rgb.copy()
        left = rect[0]
        top = rect[1]
        # rect[2], rect[3]은 너비와 높이이므로 우하단 좌표를 구하기 위해 좌상단 좌표에 각각을 더함.
        right = left + rect[2]
        bottom = top + rect[3]
        img_rgb_copy = cv2.rectangle(img_rgb_copy, (left, top), (right, bottom), color=green_rgb, thickness=2)

        cv2.imshow('image', img_rgb_copy)
        # 해당 영역이 공정 영역인 경우
        # crop 후 이미지 저장
        while True:
            key = cv2.waitKey()
            if key == ord('s'):
                # bounding box 이미지, info.txt 저장
                crop = image[top-10:bottom+10, left-10:right+10]
                file_name = f'{save_dir}\\{str(random.random())[2:6]}.png'
                # cv2.imshow('img', crop)
                cv2.imwrite(file_name, crop)
                f.write(f'[{top-10} {bottom+10} {left-10} {right+10}]')

            elif key == ord('d'):
                cv2.destroyAllWindows()
                break

def create_view(mesh, view_idx):
    obj_name = os.path.basename(path).replace('.obj', '')
    plotter = pv.Plotter(window_size=[1000, 1000], off_screen=True)
    p = plotter.add_mesh(mesh)
    plotter.background_color = 'white'
    if view_idx == 0:
        plotter.view_xy()
    elif view_idx == 1:
        plotter.view_xz()
    elif view_idx == 2:
        plotter.view_yx()
    elif view_idx == 3:
        plotter.view_yz()
    elif view_idx == 4:
        plotter.view_zx()
    elif view_idx == 5:
        plotter.view_zy()

    image_name = f'{obj_name}_00{view_idx}'
    plotter.store_image = True
    plotter.show(auto_close=False)
    image = plotter.screenshot(return_img=True)
    return image, image_name

path = 'C:\\Users\\user\\PycharmProjects\\Reaserch\\data_sample\\obj\\E_class.obj'
mesh = pv.read(path)
save_dir = 'C:\\Users\\user\\PycharmProjects\\Reaserch\\Region_proposal\\save_file'
for i in range(6):
    image, name = create_view(mesh, i)
    txt_f = f'{save_dir}\\{name}.txt'
    f = open(txt_f, 'a')
    f.write(name+'.png')
    search_region(image, f)
    f.close()
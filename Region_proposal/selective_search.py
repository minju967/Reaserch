import glob
import os.path
import sys

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
        if rect[0] == 0 and rect[3] == 999:
            continue
        img_rgb_copy = img_rgb.copy()
        left = rect[0]
        top = rect[1]
        # rect[2], rect[3]은 너비와 높이이므로 우하단 좌표를 구하기 위해 좌상단 좌표에 각각을 더함.
        right = left + rect[2]
        bottom = top + rect[3]
        img_rgb_copy = cv2.rectangle(img_rgb_copy, (left, top), (right, bottom), color=green_rgb, thickness=2)

        # cv2.imshow('image', img_rgb_copy)

        try:
            crop = image[top - 10:bottom + 10, left - 10:right + 10]
            file_name = f'{img_save_dir}\\{str(random.random())[2:6]}.png'
            # print(file_name.split('\\')[-1])
            cv2.imwrite(file_name, crop)
        except:
            crop = image[top:bottom, left:right]
            file_name = f'{img_save_dir}\\{str(random.random())[2:6]}.png'
            # print(file_name.split('\\')[-1])
            cv2.imwrite(file_name, crop)

        print(file_name.split('\\')[-1])

        # 해당 영역이 공정 영역인 경우
        while False:
            key = cv2.waitKey()
            if key == ord('s'):
                # bounding box 이미지, info.txt 저장
                try:
                    crop = image[top-10:bottom+10, left-10:right+10]
                    file_name = f'{img_save_dir}\\{str(random.random())[2:6]}.png'
                    # cv2.imshow('img', crop)
                    cv2.imwrite(file_name, crop)
                    f.write(f'[{top - 10} {bottom + 10} {left - 10} {right + 10}]')
                except:
                    crop = image[top:bottom, left:right]
                    file_name = f'{img_save_dir}\\{str(random.random())[2:6]}.png'
                    # cv2.imshow('img', crop)
                    cv2.imwrite(file_name, crop)
                    f.write(f'[{top} {bottom} {left} {right}]')
                cv2.destroyAllWindows()
                break
            elif key == ord('d'):
                cv2.destroyAllWindows()
                break
            elif key == ord('q'):
                sys.exit()
            elif key == ord('p'):
                f.write(f'[]')
                cv2.destroyAllWindows()
                return 0
    return 1

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

def main():
    dir_path = 'D:\\project\\data_alignment\\D_train'
    data = glob.glob(dir_path + '\\*.obj')
    img_save_dir = 'C:\\Users\\user\\PycharmProjects\\Reaserch\\Region_proposal\\save_file\\cut_image'
    # txt_save_dir = 'C:\\Users\\user\\PycharmProjects\\Reaserch\\Region_proposal\\save_file\\wire_position'
    save_f = 'C:\\Users\\user\\PycharmProjects\\Reaserch\\Region_proposal\\save_file\\D_save.txt'
    w_file = open(save_f, 'a')
    r_file = open(save_f, 'r')
    files = r_file.readlines()
    files = [file.strip() for file in files]

    try:
        for path in data:
            if path.strip() not in files:
                w_file.write(path+'\n')
                print(path.strip())
            else:
                print(f'exist file: {path}')
                continue

            mesh = pv.read(path)

            for i in range(6):
                image, name = create_view(mesh, i)
                # txt_f = f'{txt_save_dir}\\{name}.txt'
                # f = open(txt_f, 'a')
                # f.write(name+'.png')
                # result = search_region(image, f)
                result = search_region(image, None)
                if result == 0:
                    # f.close()
                    continue
                # f.close()
            print()

    except Exception as e:
        print(e)
        w_file.close()


image = cv2.imread('C:\\Users\\user\\PycharmProjects\\Reaserch\\110282_311_011.png')
image = cv2.resize(image, (1000,1000))
img_rgb=cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
_, regions = selectivesearch.selective_search(img_rgb, scale=100, min_size=3000)
# cand_rects = [cand['rect'] for cand in regions if cand['size'] > 10000]
cand_rects = []
for cand in regions:
    width = cand['rect'][2]
    height = cand['rect'][3]
    if max(width, height) // min(width, height) < 5:
        cand_rects.append(cand['rect'])

green_rgb = (125, 255, 51) # bounding box
red_rgb = (107, 0, 0) # bounding box color
blue_rgb = (0, 43, 198)
img_rgb_copy = img_rgb.copy() # 이미지 복사
color = [green_rgb, red_rgb, blue_rgb]

for rect in cand_rects[1:]:
  left = rect[0]
  top = rect[1]
  # rect[2], rect[3]은 너비와 높이이므로 우하단 좌표를 구하기 위해 좌상단 좌표에 각각을 더함.
  right = left + rect[2]
  bottom = top + rect[3]
  img_rgb_copy = cv2.rectangle(img_rgb_copy, (left, top), (right, bottom), color=random.choice(color), thickness=2)

plt.figure(figsize=(8, 8))
plt.imshow(img_rgb_copy)
plt.show()

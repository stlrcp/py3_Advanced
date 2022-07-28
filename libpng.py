# import cv2
# from skimage import io
# path = r"C:\迅雷下载\train\100.jpg"
# image = io.imread(path)
# print(image.shape)
# image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
# print(image.shape)
# cv2.imencode('.png', image)[1].tofile(path)
# print(len(cv2.imencode('.png', image)[1]))

import os
from tqdm import tqdm
import cv2
from skimage import io
path = r"C:\迅雷下载\train"
filelist = os.listdir(path)
# print(filelist)
for i in tqdm(filelist):
    image = io.imread(path+"\\"+i)   # image = io.imread(os.path.join(path, i))
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGRA)
    cv2.imencode('.png', image)[1].tofile(path+"\\"+i)
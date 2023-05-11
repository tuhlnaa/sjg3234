import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

img = mpimg.imread('a01.jpg')
print(img.shape)

from operator import add
from functools import reduce

# =========================================================
# 【影像分解】
def split4(image):
    half_split = np.array_split(image, 2)
    print(len(half_split))
    res = map(lambda x: np.array_split(x, 2, axis=1), half_split)
    return reduce(add, res)


split_img = split4(img)

fig, axs = plt.subplots(2, 2, num = "Split") # 建立plt畫布 
axs[0, 0].imshow(split_img[0])
axs[0, 1].imshow(split_img[1])
axs[1, 0].imshow(split_img[2])
axs[1, 1].imshow(split_img[3])

print(split_img[0].shape)
print(split_img[0].shape)
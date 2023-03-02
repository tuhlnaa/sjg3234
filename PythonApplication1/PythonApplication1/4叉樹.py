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

# =========================================================
# 【影像合成】
def concatenate4(north_west, north_east, south_west, south_east):
    top = np.concatenate((north_west, north_east), axis=1)
    bottom = np.concatenate((south_west, south_east), axis=1)
    return np.concatenate((top, bottom), axis=0)

full_img = concatenate4(split_img[0], split_img[1], split_img[2], split_img[3])

plt.figure("Reconstruct")  # 建立plt畫布 
plt.imshow(full_img)



def calculate_mean(img):
    return np.mean(img, axis=(0, 1))

means = np.array(list(map(lambda x: calculate_mean(x), split_img))).astype(int).reshape(2,2,3)
print(means)

plt.figure("mean")  # 建立plt畫布 
plt.imshow(means)
plt.show()

# =========================================================
# 【4叉樹】
def checkEqual(myList):
    first=myList[0]
    return all((x==first).all() for x in myList)

class QuadTree:
    
    def insert(self, img, level = 0):
        self.level = level
        self.mean = calculate_mean(img).astype(int)
        self.resolution = (img.shape[0], img.shape[1])
        self.final = True
        
        if not checkEqual(img):
            split_img = split4(img)
            
            self.final = False
            self.north_west = QuadTree().insert(split_img[0], level + 1)
            self.north_east = QuadTree().insert(split_img[1], level + 1)
            self.south_west = QuadTree().insert(split_img[2], level + 1)
            self.south_east = QuadTree().insert(split_img[3], level + 1)

        return self
    
    def get_image(self, level):
        if(self.final or self.level == level):
            return np.tile(self.mean, (self.resolution[0], self.resolution[1], 1))
        
        return concatenate4(
            self.north_west.get_image(level), 
            self.north_east.get_image(level),
            self.south_west.get_image(level),
            self.south_east.get_image(level))

plt.figure("QuadTree")  # 建立plt畫布

quadtree = QuadTree().insert(img)

plt.imshow(quadtree.get_image(1))
plt.show()
plt.imshow(quadtree.get_image(3))
plt.show()
plt.imshow(quadtree.get_image(7))
plt.show()
plt.imshow(quadtree.get_image(10))
plt.show()
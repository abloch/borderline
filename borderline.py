"""draws and returns the border of an image with an absolute white background as dots and image"""
from sys import argv
from cv2 import cv2 as cv
import numpy as np
import json

def is_background(pixel):
    return pixel == 255  # absolute white


def is_foreground(pixel):
    return pixel < 255  # non absolute white


def has_backgroung_neighbours_with_diagonal(gray_image, x, y):
    neighbours = [
        gray_image[y-1,x-1], gray_image[y-1,x], gray_image[y-1,x+1],
        gray_image[y,x-1], gray_image[y,x+1],
        gray_image[y+1,x-1], gray_image[y+1,x], gray_image[y+1,x+1]
    ]
    return any([is_background(neighbour) for neighbour in neighbours])


def has_background_neighbours(gray_image, x, y):
    neighbours = [
        gray_image[y-1,x],
        gray_image[y,x-1], gray_image[y,x+1],
        gray_image[y+1,x]
    ]
    return any([is_background(neighbour) for neighbour in neighbours])


def find_neighbours(gray):
    dots = []
    height = img.shape[0]
    width = img.shape[1]
    
    res = np.zeros(gray.shape)
    for x in range(1, width-2):
        for y in range(1, height-1):
            if is_foreground(gray[y, x]) and has_background_neighbours(gray, x, y):
                dots.append([x, y])
                res[y, x] = 255
    return dots, res

filename = argv[1]
img = cv.imread(filename)

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
dots, res = find_neighbours(gray)

cv.imwrite(f"result_{filename}", res)
json.dump(dots, open(f"{filename}.json", "w"))
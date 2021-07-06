import os
import cv2 as cv
import sys
import random
import xml.etree.ElementTree as ET
import numpy as np
import re

INPUT_PATH = "Dataset/"
category_list = []
imgs_list = []
annotations_list = []
bounding_box_list = []
title_images_list = []


def split_title(title):
    r"""
    Split text of the directory
    :param title: text to split
    :return: text with the tabulations
    """
    title = title[0].upper() + title[1:]
    folder = re.findall('[A-Z][^A-Z]*', title)
    result = ""
    for i, item in enumerate(folder):
        result += str(item) + (" " if (i + 1) != len(folder) else "")

    return result


def draw_description(img, text):
    r"""
    Draw description image
    :param text: image description
    :param img: image in which to insert the descrition
    :return: image with description
    """

    bottom = int(0.04 * img.shape[0])
    img = cv.copyMakeBorder(img, 0, bottom, 0, 0, cv.BORDER_CONSTANT, None, (255, 255, 255))

    height, _, _ = img.shape
    cv.putText(img, text, (0, height - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    return img


def stackImages(scale, img_array):
    r"""
    Stack the images based on the number of them by rows and columns.
    Resize the images.
    :param scale: scale factor.
    :param img_array: array of images.
    :return: array of images to show.
    """

    rows = len(img_array)
    cols = len(img_array[0])

    rowsAvailable = isinstance(img_array[0], list)

    width = img_array[0][0].shape[1]
    height = img_array[0][0].shape[0]

    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):

                if img_array[x][y].shape[:2] == img_array[0][0].shape[:2]:
                    img_array[x][y] = cv.resize(img_array[x][y], (0, 0), None, scale, scale)
                else:
                    img_array[x][y] = cv.resize(img_array[x][y], (img_array[0][0].shape[1], img_array[0][0].shape[0]),
                                                None, scale, scale)

                if len(img_array[x][y].shape) == 2:
                    img_array[x][y] = cv.cvtColor(img_array[x][y], cv.COLOR_GRAY2BGR)

        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows

        for x in range(0, rows):
            hor[x] = np.hstack(img_array[x])
        ver = np.vstack(hor)

    else:
        for x in range(0, rows):

            if img_array[x].shape[:2] == img_array[0].shape[:2]:
                img_array[x] = cv.resize(img_array[x], (0, 0), None, scale, scale)
            else:
                img_array[x] = cv.resize(img_array[x], (img_array[0].shape[1], img_array[0].shape[0]), None, scale,
                                         scale)

            if len(img_array[x].shape) == 2:
                img_array[x] = cv.cvtColor(img_array[x], cv.COLOR_GRAY2BGR)

        hor = np.hstack(img_array)
        ver = hor

    return ver


argv = sys.argv

if len(argv) > 1:
    INPUT_PATH = (argv[1])

dirs = os.listdir(INPUT_PATH)

category_list.append(random.randint(0, len(dirs) - 1))
category_list.append(random.randint(0, len(dirs) - 1))
category_list.append(random.randint(0, len(dirs) - 1))
category_list.append(random.randint(0, len(dirs) - 1))

for i in range(0, 4):
    alpha = 0.5
    bounding_box_list.clear()

    while True:
        index_category = category_list[i]
        imgs = os.listdir(INPUT_PATH + dirs[index_category] + "/imgs/")
        annotations = os.listdir(INPUT_PATH + dirs[index_category] + "/annotations/")

        category_list[i] = random.randint(0, len(dirs) - 1)

        if len(imgs) != 0:
            break

    index_img = random.randint(0, len(imgs) - 1)

    # Parse file xml
    tree = ET.parse(INPUT_PATH + dirs[index_category] + "/annotations/" + annotations[index_img])
    root = tree.getroot()

    # Get all bounding boxes
    j = 6
    while True:
        try:
            object = root[j]
            box = object[4]
            x_min, y_min, x_max, y_max = int(box[0].text), int(box[1].text), int(box[2].text), int(box[3].text)
            bounding_box_list.append([[x_min - 1, y_min - 1], [x_max - 1, y_max - 1]])
            j += 1
        except:
            break

    print(f"{i + 1}: {annotations[index_img]}")
    # Read the image
    img_read = cv.imread(INPUT_PATH + dirs[index_category] + "/imgs/" + imgs[index_img])

    # Mask
    mask = np.zeros_like(img_read[:, :, 0])

    for j, box in enumerate(bounding_box_list):
        cv.rectangle(img_read, box[0], box[1], (0, 0, 255), 5)
        polygon = np.array([[bounding_box_list[j][0]], [[bounding_box_list[j][1][0], bounding_box_list[j][0][1]]],
                            [bounding_box_list[j][1]], [[bounding_box_list[j][0][0], bounding_box_list[j][1][1]]]])
        cv.fillConvexPoly(mask, polygon, 1)

    # Get polygon
    img = cv.bitwise_and(img_read, img_read, mask=mask)
    img = cv.addWeighted(img_read.copy(), alpha, img, 1 - alpha, 0)
    img = cv.resize(img, (400, 400))
    imgs_list.append(img)

    title = dirs[index_category]
    title_images_list.append(split_title(title))

imgs_stack = stackImages(1, ([draw_description(imgs_list[0], title_images_list[0]),
                              draw_description(imgs_list[1], title_images_list[1])],
                             [draw_description(imgs_list[2], title_images_list[2]),
                              draw_description(imgs_list[3], title_images_list[3])]))

# Show images
cv.imshow("Images", imgs_stack)
cv.waitKey(0)

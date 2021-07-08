import os
import cv2 as cv
import sys
import xml.etree.ElementTree as ET
import numpy as np
import re
from tkinter import Label, Tk, Button, Entry, DISABLED
from PIL import Image
from PIL import ImageTk


def split_title(title):
    """
    Slit the text of the directory by upper case.
    """
    title = title[0].upper() + title[1:]
    folder = re.findall('[A-Z][^A-Z]*', title)
    result = ""
    for i, item in enumerate(folder):
        result += str(item) + (" " if (i + 1) != len(folder) else "")

    return result


def draw_description(img, text):
    """
    Insert the description on the type of monument on the image.
    """
    bottom = int(0.04 * img.shape[0])
    img = cv.copyMakeBorder(img, 0, bottom, 0, 0, cv.BORDER_CONSTANT, None, (255, 255, 255))

    height, _, _ = img.shape
    cv.putText(img, text, (0, height - 5), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    return img


def convert_img(img_to_convert):
    """
    Convert opencv image in PIL image.
    """

    # Split color
    b, g, r = cv.split(img_to_convert)
    img_to_convert = cv.merge((r, g, b))

    img_to_convert = Image.fromarray(img_to_convert)
    img = ImageTk.PhotoImage(img_to_convert)

    return img


def load_images(INPUT_PATH):
    """
    Load all images of the dataset.
    """
    imgs_list = []
    annotations_list = []
    bounding_box_list = []
    # labels_list = []

    dirs = os.listdir(INPUT_PATH)

    for index_dir, dir in enumerate(dirs):
        bounding_box_list.clear()
        # labels_list.clear()

        imgs = os.listdir(INPUT_PATH + dirs[index_dir] + "/imgs/")
        annotations = os.listdir(INPUT_PATH + dirs[index_dir] + "/annotations/")

        for index_xml, xml in enumerate(annotations):
            bounding_box_list.clear()

            # Draw bounding box
            tree = ET.parse(INPUT_PATH + dirs[index_dir] + "/annotations/" + annotations[index_xml])
            root = tree.getroot()

            # Get all bounding boxes
            j = 6
            while True:
                try:
                    object = root[j]
                    box = object[4]

                    # Bounding box
                    x_min, y_min, x_max, y_max = int(box[0].text), int(box[1].text), int(box[2].text), int(box[3].text)
                    bounding_box_list.append([[x_min - 1, y_min - 1], [x_max - 1, y_max - 1]])

                    # Labels
                    # tag_name = object[0]
                    # labels_list.append(tag_name.text)

                    j += 1
                except:
                    break

            # Read the image
            img_read = cv.imread(INPUT_PATH + dirs[index_dir] + "/imgs/" + imgs[index_xml])

            # Mask
            mask = np.zeros_like(img_read[:, :, 0])

            for j, box in enumerate(bounding_box_list):
                # Draw rectangle bounding box
                cv.rectangle(img_read, box[0], box[1], (0, 0, 255), 5)
                polygon = np.array(
                    [[bounding_box_list[j][0]], [[bounding_box_list[j][1][0], bounding_box_list[j][0][1]]],
                     [bounding_box_list[j][1]], [[bounding_box_list[j][0][0], bounding_box_list[j][1][1]]]])
                cv.fillConvexPoly(mask, polygon, 1)

                # Draw rectangle labels
                # x_start, y_start = box[0]
                # x_end, y_end = box[1][0], y_start
                # cv.rectangle(img_read, (x_start + 7, y_start + 5), (x_end - 5, y_end + 30), (255, 255, 255), cv.FILLED)
                # cv.putText(img_read, labels_list[j], (x_start + 7, y_start + 25), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 0),2)

            # Get polygon
            alpha = 0.5
            img = cv.bitwise_and(img_read, img_read, mask=mask)
            img = cv.addWeighted(img_read.copy(), alpha, img, 1 - alpha, 0)
            img = cv.resize(img, (400, 400))
            img = draw_description(img, split_title(dir))

            # cv.imwrite(INPUT_PATH + dirs[index_dir] + "/bounding_box/", imgs[index_xml])

            imgs_list.append(img)
            annotations_list.append(xml)

    return imgs_list, annotations_list


def back_img():
    """
    Action button back.
    """
    global index_img, label, images, button_back, button_next, xml
    index_img -= 1

    label.grid_forget()
    img = convert_img(images[index_img])
    label = Label(image=img)
    label.photo = img

    button_back = Button(window, text="<<", command=lambda: back_img())
    button_next = Button(window, text=">>", command=lambda: forward_img())

    if index_img == 0:
        button_back = Button(window, text="<<", state=DISABLED)

    label.grid(row=0, column=0, columnspan=3)
    button_back.grid(row=1, column=0)
    button_next.grid(row=1, column=2)
    window.title(xml[index_img])


def forward_img():
    """
    Action forward button.
    """
    global index_img, label, images, button_back, button_next, xml
    index_img += 1

    label.grid_forget()
    img = convert_img(images[index_img])
    label = Label(image=img)
    label.photo = img

    button_back = Button(window, text="<<", command=lambda: back_img())
    button_next = Button(window, text=">>", command=lambda: forward_img())

    if index_img == len(images) - 1:
        button_next = Button(window, text=">>", state=DISABLED)

    label.grid(row=0, column=0, columnspan=3)
    button_back.grid(row=1, column=0)
    button_next.grid(row=1, column=2)
    window.title(xml[index_img])


def submit_file():
    """
    Find specific file.
    """
    global images, xml, label, button_back, button_next, index_img

    index_filter = [index for index, file in enumerate(xml) if file == text_input.get() + str(".xml")]

    if len(index_filter) != 0:
        index_img = index_filter[0]
        img = convert_img(images[index_img])

        label.grid_forget()
        label = Label(image=img)
        label.photo = img

        button_back = Button(window, text="<<", command=lambda: back_img())
        button_next = Button(window, text=">>", command=lambda: forward_img())

        if index_img == len(images) - 1:
            button_next = Button(window, text=">>", state=DISABLED)
        elif index_img == 0:
            button_back = Button(window, text="<<", state=DISABLED)

        label.grid(row=0, column=0, columnspan=3)
        button_back.grid(row=1, column=0)
        button_next.grid(row=1, column=2)
        window.title(xml[index_img])


def exit():
    """
    Action exit button.
    """
    window.quit()


INPUT_PATH = "Dataset/"
index_img = 0
argv = sys.argv

if len(argv) > 1:
    INPUT_PATH = (argv[1])

images, xml = load_images(INPUT_PATH)

# Window 1  (Show images)
window = Tk()
# window.title("Cultural Heritage Pesaro")

_img = images[index_img]
_img = convert_img(_img)
label = Label(image=_img)
label.grid(row=0, column=0, columnspan=3)

button_back = Button(window, text="<<", command=lambda: back_img())
button_next = Button(window, text=">>", command=lambda: forward_img())
button_exit = Button(window, text="Exit", command=exit())
window.title(xml[index_img])

if index_img == 0:
    button_back = Button(window, text="<<", state=DISABLED)
elif index_img == len(images) - 1:
    button_next = Button(window, text=">>", state=DISABLED)

button_back.grid(row=1, column=0)
button_exit.grid(row=1, column=1)
button_next.grid(row=1, column=2)

# Window 2 (Submit file)
window_text = Tk()
window_text.title("Submit file")

text_input = Entry(window_text, width=50)
text_input.pack()
text_input.insert(0, "")

button_submit = Button(window_text, text="Submit", command=submit_file)
button_submit.pack()

# Main loop
window.mainloop()
window_text.mainloop()

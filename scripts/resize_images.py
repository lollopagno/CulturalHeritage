import os
import cv2 as cv
import sys

INPUT_PATH = "Da_Etichettare/"
OUTPUT_PATH = "Risoluzioni/"

argv = sys.argv

r1 = int(argv[1])
r2 = int(argv[2])
RESOLUTION = f"{r1}X{r2}"

if len(argv) > 3:
    INPUT_PATH = (argv[3])

if len(argv) > 4:
    OUTPUT_PATH = argv[4]

try:
    # Create directory
    os.mkdir(OUTPUT_PATH + RESOLUTION)
except:
    pass

for img in os.listdir(INPUT_PATH):

    _img = cv.imread(INPUT_PATH + img)
    h, w, _ = _img.shape

    if h > w:
        resized = cv.resize(_img, (r2, r1))
    else:
        resized = cv.resize(_img, (r1, r2))

    cv.imwrite(OUTPUT_PATH + RESOLUTION + "/" + img, resized)

print("Finished!")

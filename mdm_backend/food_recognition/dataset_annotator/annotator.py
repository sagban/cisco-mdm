import cv2
import numpy as np 
import matplotlib.pyplot as plt
import os

IMAGE_DIR = os.path.join(os.getcwd(), "images")
ANNOTATION_DIR = os.path.join(os.getcwd(), "annotations")

annotation_strings = {}
# Load all the image files
image_files = [f for f in os.listdir(IMAGE_DIR)]
print(image_files)

click_count = 0
x1, x2, y1, y2 = (0, 0, 0, 0)

filename = "" 
dirname = IMAGE_DIR[IMAGE_DIR.rfind("/")+1:]

def write_annotations(annotation_strings):        
    for k, v in annotation_strings.items():
        with open(os.path.join(ANNOTATION_DIR, k[:k.find('.')]+".txt"), "w") as f:
            f.write(v)

def onclick(event):
    global click_count, x1, y1, x2, y2
    global annotation_strings, filename, dirname
    click_count += 1
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    if click_count %2 != 0:
        x1, y1 = event.x, event.y
    else:
        x2, y2 = event.x, event.y
        annotation_strings[filename] = "{}\n{} {} {} {} {}".format(filename[:filename.find(".")], x1, y1, x2, y2, dirname)
                 
for i in image_files:
    fig, ax = plt.subplots()
    filepath = os.path.join(IMAGE_DIR, i)
    img = cv2.imread(filepath)
    ax.imshow(img)    
    filename = i
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    if click_count % 10 == 0:
        write_annotations(annotation_strings)
        annotation_strings.clear()

if len(annotation_strings) != 0:
    write_annotations(annotation_strings)
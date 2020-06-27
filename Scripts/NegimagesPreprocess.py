import os
import cv2
#os.chdir('G:/neg/')
os.chdir('G:/pos/')
image_number = 1

def organizeimages():
    image_number = 1
    for filename in os.listdir():
        if filename.endswith(".jpg") or filename.endswith(".bmp"): 
             os.rename(filename, str(image_number)+".jpg")
             image_number += 1
        else:
            continue

def gray_resize():
    image_number = 1
    for filename in os.listdir():
        img = cv2.imread(str(image_number)+".jpg",cv2.IMREAD_GRAYSCALE)
        resized_image = cv2.resize(img, (65,45))
        cv2.imwrite(str(image_number)+".jpg",resized_image)
        image_number += 1 


def create_path_files():
    for filename in os.listdir():
        line = "neg" +'/'+ filename +'\n'
        with open('neg_path.txt','a') as f:
            f.write(line)

gray_resize()

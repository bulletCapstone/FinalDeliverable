import graphviz
import sys, subprocess
import cv2
import numpy as np
import glob
# visualizer.py < textfile

count = 0
currentLine = ""
for line in sys.stdin:
    if line != "}\n":
        currentLine += line
    else:
        count+=1
        currentLine += line
        src = graphviz.Source(currentLine)
        print(count)
        number = str(count)
        number = number.zfill(6)
        src.render('bvhtree/'+number,view=False,format='png')
        currentLine = ""




img_array = []
files = glob.glob('./bvhtree/*.png')
files.sort()
shape = 1000, 1000

for filename in files:
    print(filename)
    img = cv2.imread(filename)
    resized = cv2.resize(img,shape)
    # height, width, layers = img.shape
    # size = (width,height)
    img_array.append(resized)
out = cv2.VideoWriter('project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 0.8, shape)
 
for i in range(len(img_array)):
    out.write(img_array[i])
out.release()


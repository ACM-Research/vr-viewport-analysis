import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# import os
# print(os.getcwd())

img = None
data = pd.read_csv('Scripts/csv/POI5.csv')
rows = data.values

index = 0
for row in rows:
    uncropped = Image.open('Salient Feature Traces/5/frame' + str(index * 30 + 1) + '.jpg')
    area = (135, 45, 2135, 1110) # using frames with grid rather than original video data
    cropped_img = uncropped.crop(area)
    if img is None:
        img = plt.imshow(cropped_img)
    else:
        img.set_data(cropped_img)
    
    frame = row[0]
    [x1, y1, x2, y2] = np.array(row[1:5]) / 2 # approx due to using grid

    [p.remove() for p in reversed(plt.gca().patches)] # remove previous squares

    # draw first in red, second in green
    rect = patches.Rectangle((x1,y1),30,30,linewidth=1,edgecolor='r',facecolor='none')
    plt.gca().add_patch(rect)
    rect = patches.Rectangle((x2,y2),30,30,linewidth=1,edgecolor='g',facecolor='none')
    plt.gca().add_patch(rect)

    index += 1
    plt.pause(1)
    plt.draw()
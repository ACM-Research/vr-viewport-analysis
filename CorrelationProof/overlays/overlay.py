import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

import os
print(os.getcwd())

def play_video():
    img = None
    vid_id = "23"

    POI_data = pd.read_excel('Finished POI Spreadsheets/' + vid_id + ' POI Finished.xlsx')
    POI_rows = POI_data.values

    trace_data = pd.read_csv("Experiment Data/Traces/0Z4VWJ/0Z4VWJ_" + vid_id + ".csv")
    trace_rows = trace_data.values

    index = 0
    for row in POI_rows:
        # get frame
        im = Image.open('Experiment Data/SampleVideos/SourceFrames/' + vid_id + '/frame' + str(index * 30 + 1) + '.jpg')
        if img is None:
            img = plt.imshow(im)
        else:
            img.set_data(im)
        
        # draw manually selected salient features
        frame = row[0]
        draw_patches(plt, row)
        
        # draw user trace points
        trace_row = trace_rows[index * 30]
        arr = [trace_row[5], trace_row[6], trace_row[7]]
        x, y = ConvVec2Angl(arr)
        x = ((x+180)/360)*im.size[0]
        y = ((90-y)/180)*im.size[1]
        draw_rectrangle(plt, x, y, 'g')

        # redraw
        index += 1
        plt.pause(0.5)
        plt.draw()

def draw_patches(plt, row):
    [p.remove() for p in reversed(plt.gca().patches)]
    for i in range(1, len(row), 2):
        cx = row[i]
        cy = row[i+1]
        draw_rectrangle(plt, cx, cy, 'r')

def draw_rectrangle(plt, x1, y1, color):
    rect = patches.Rectangle((x1,y1),30,30,linewidth=1,edgecolor=color,facecolor='none')
    plt.gca().add_patch(rect)

def cart2sph(x,y,z):
    azimuth = np.arctan2(y,x)
    elevation = np.arctan2(z,np.sqrt(x**2 + y**2))
    r = np.sqrt(x**2 + y**2 + z**2)
    return azimuth, elevation, r

def ConvVec2Angl(vector):
    # TODO maybe better way to get pitch/yaw
    # https://stackoverflow.com/questions/2782647/how-to-get-yaw-pitch-and-roll-from-a-3d-vector
    t, p, r = cart2sph(vector[2], vector[0], vector[1])
    theta = math.degrees(t)
    phi = math.degrees(p)
    return theta, phi

def main():
    play_video()

if __name__ == "__main__":
    main()
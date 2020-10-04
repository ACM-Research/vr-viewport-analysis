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
    vid_id = "24"

    poi_data = pd.read_excel('Finished POI Spreadsheets/' + vid_id + ' POI Finished.xlsx')
    poi_rows = poi_data.values

    trace_rows_all = []
    user_folders = [trace for trace in os.listdir('CorrelationProof/overlays/GroupByVideos/' + vid_id)]
    for user in user_folders:
        trace_data = pd.read_csv('CorrelationProof/overlays/GroupByVideos/' + vid_id + '/' + user)
        trace_rows = trace_data.values
        trace_rows_all.append(trace_rows)

    index = 0
    for row in poi_rows:
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
        for trace_rows in trace_rows_all:
            trace_row = trace_rows[index * 30]
            arr = [trace_row[5], trace_row[6], trace_row[7]]
            x, y = convvec2angl(arr)
            x = ((x+180)/360)*im.size[0]
            y = ((90-y)/180)*im.size[1]
            draw_rectrangle(plt, x, y, 'g')

        # redraw
        index += 1
        plt.pause(1)
        plt.draw()


def draw_patches(plotter, row):
    [p.remove() for p in reversed(plotter.gca().patches)]
    for i in range(1, len(row), 2):
        cx = row[i]
        cy = row[i+1]
        draw_rectrangle(plotter, cx, cy, 'r')


def draw_rectrangle(plotter, x1, y1, color):
    rect = patches.Rectangle((x1, y1), 60, 60, linewidth=3, edgecolor=color, facecolor='none')
    plotter.gca().add_patch(rect)


def cart2sph(x, y, z):
    azimuth = np.arctan2(y, x)
    elevation = np.arctan2(z, np.sqrt(x**2 + y**2))
    r = np.sqrt(x**2 + y**2 + z**2)
    return azimuth, elevation, r


def convvec2angl(vector):
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
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import json

import os
print(os.getcwd())


def play_video(draw=True):
    img = None
    vid_id = "24"

    poi_data = pd.read_excel(f'Finished POI Spreadsheets/{vid_id} POI Finished.xlsx')
    poi_rows = poi_data.values

    trace_rows_all = []
    user_folders = [trace for trace in os.listdir(f'CorrelationProof/overlays/GroupByVideos/{vid_id}')]
    for user in user_folders:
        trace_data = pd.read_csv(f'CorrelationProof/overlays/GroupByVideos/{vid_id}/{user}')
        trace_rows = trace_data.values
        trace_rows_all.append(trace_rows)

    # get frame size if not drawing
    im_size0 = 0
    im_size1 = 0
    if not draw:
        im = Image.open(f'Experiment Data/SampleVideos/SourceFrames/{vid_id}/frame1.jpg')
        im_size0 = im.size[0]
        im_size1 = im.size[1]

    index = 0
    process_data = []
    for row in poi_rows:
        print(index)

        # get frame
        if draw:
            im = Image.open(f'Experiment Data/SampleVideos/SourceFrames/{vid_id}/frame{index * 30 + 1}.jpg')
            im_size0 = im.size[0]
            im_size1 = im.size[1]
            if img is None:
                img = plt.imshow(im)
            else:
                img.set_data(im)

        # draw manually selected salient features
        frame = row[0]
        salient_points = draw_patches(plt, row, draw)

        # draw user trace points
        all_user_points = []
        for trace_rows in trace_rows_all:
            trace_row = trace_rows[index * 30]
            arr = [trace_row[5], trace_row[6], trace_row[7]]
            x, y = convvec2angl(arr)
            x = ((x+180)/360)*im_size0
            y = ((90-y)/180)*im_size1
            all_user_points.append((x, y))
            if draw:
                draw_rectangle(plt, x, y, 'g')

        # add to output data
        process_data.append({'index': index, 'salient': salient_points, 'trace': all_user_points})

        # redraw
        index += 1
        if draw:
            plt.pause(1)
            plt.draw()

    return process_data


def draw_patches(plotter, row, draw=True):
    if draw:
        [p.remove() for p in reversed(plotter.gca().patches)]
    salient_points = []
    for i in range(1, len(row), 2):
        cx = row[i]
        cy = row[i+1]
        if not math.isnan(cx) and not math.isnan(cy):
            salient_points.append((cx, cy))
        if draw:
            draw_rectangle(plotter, cx, cy, 'r')
    return salient_points


def draw_rectangle(plotter, x1, y1, color):
    rect = patches.Rectangle((x1, y1), 60, 60, linewidth=3, edgecolor=color, facecolor='none')
    plotter.gca().add_patch(rect)


def convvec2angl(vector):
    phi = math.degrees(math.asin(vector[1]))
    theta = math.degrees(math.atan2(vector[0], vector[2]))
    return theta, phi


def main():
    # Change False to True to show overlay
    # However, False will run a lot faster (for outputting data file)
    data = play_video(False)
    with open("CorrelationProof/overlays/data.txt", 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()

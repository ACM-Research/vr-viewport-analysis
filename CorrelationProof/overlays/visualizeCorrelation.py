import json
import random
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


THRES = 60
vid_id = 24 # TODO


def pointsToXY(points):
    x_list = [x for [x, y] in points]
    y_list = [y for [x, y] in points]
    return x_list, y_list


def dist(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def animate(f):
    global ij, total, img, vid_id, circleCount, totalArea, pointCount

    # graph salient points
    points = data[f]["salient"]
    graph.set_data(pointsToXY(points))

    #show image
    im = Image.open(f"Experiment Data/SampleVideos/SourceFrames/{vid_id}/frame{ij * 30 + 1}.jpg")  # .transpose(Image.FLIP_TOP_BOTTOM)
    if img is None:
        img = axes[0].imshow(im)
    else:
       img.set_data(im)

    # remove circles from last animation frame
    for obj in axes[0].findobj(match=type(plt.Circle(1, 1))):
        obj.remove()

    # draw circles for this frame
    for salient in points:
        circle1 = plt.Circle((salient[0], salient[1]), THRES, color='r', fill=False)
        axes[0].add_artist(circle1)

    # process trace points into:
    # 1. inRangePoints:  points inside of at least one salient feature's threshold radius
    # 2. outRangePoints: points not inside any salient feature's threshold radius
    points2 = data[f]["trace"]
    inRangePoints = []
    outRangePoints = []
    for p in points2:
        found = False
        for j in points:
            if dist(p, j) < THRES * THRES:
                found = True
                break
        if found:
            inRangePoints.append(p)
        else:
            outRangePoints.append(p)

    # keep track of statistics
    p = len(inRangePoints) / len(points2) * 100
    line.append(p)
    ij += 1
    total += len(inRangePoints) 
    pointCount += len(points2)
    circleArea = len(points)*3.14*THRES*THRES / 1920000
    totalArea += circleArea
    circleCount += len(points)
    #print("Average: " + str(total / ij)+ ", " + str(circleArea)) 
    print( (1.0*total/pointCount) / (1.0*totalArea/circleCount))
    # display points for image subplot
    in_range.set_data(pointsToXY(inRangePoints))
    others.set_data(pointsToXY(outRangePoints))

    # display chart for percentage of points covered in threshold
    axes[1].cla()
    axes[1].plot(np.arange(ij), line)

    return graph, in_range, others


# read in vid 24's data
data = []
with open("CorrelationProof/overlays/data.txt", 'r') as f:
    data = json.load(f)

# setup subplots and init image subplot
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 7))
axes[0].set_xlim([0, 3840])
axes[0].set_ylim([1920, 0])
fig.tight_layout()

# setup the three types of points for image subplot
graph, = axes[0].plot([], [], 'o')
in_range, = axes[0].plot([], [], 'o')
others, = axes[0].plot([], [], 'o')

# some variables to keep track of statistics
ij = 0
line = []
total = 0
img = None
circleCount = 0
totalArea = 0
pointCount = 0


# animation (59 goes up to 59 * 30 + 1 = 1771'th frame)
ani = FuncAnimation(fig, animate, frames=59, interval=500, repeat=False)

# uncomment to save (alternate comment with plt.show())
# ani.save('CorrelationProof/overlays/demo.gif', writer='imagemagick', fps=3)

# show animation (alternate comment with ani.save())
plt.show()
print(1.0*totalArea/circleCount)
print(1.0*total/ij)
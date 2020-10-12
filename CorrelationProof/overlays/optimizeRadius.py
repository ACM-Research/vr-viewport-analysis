import json
import random
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def pointsToXY(points):
    x_list = [x for [x, y] in points]
    y_list = [y for [x, y] in points]
    return x_list, y_list


def dist(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def animate(f, th):
    global ij, total, img, vid_id, circleCount, totalArea, pointCount

    # graph salient points
    points = data[f]["salient"]

    # process trace points into:
    # 1. inRangePoints:  points inside of at least one salient feature's threshold radius
    # 2. outRangePoints: points not inside any salient feature's threshold radius
    points2 = data[f]["trace"]
    inRangePoints = []
    outRangePoints = []
    for p in points2:
        found = False
        for j in points:
            if dist(p, j) < th * th:
                found = True
                break
        if found:
            inRangePoints.append(p)
        else:
            outRangePoints.append(p)

    p = len(inRangePoints) / len(points2) * 100
    ij += 1
    total += len(inRangePoints) 
    pointCount += len(points2)
    circleArea = len(points)*3.14*th*th / 1920000
    totalArea += 1920000
    circleCount += len(points)*3.14*th*th


# read in vid 24's data
data = []
with open("CorrelationProof/overlays/data.txt", 'r') as f:
    data = json.load(f)

# some variables to keep track of statistics
ij = 0
total = 0
circleCount = 0
totalArea = 0
pointCount = 0

result_x = []
result_y = []
result_points = []

max_radius = 200

for th in range(1, max_radius, 2):
    ij = 0
    total = 0
    circleCount = 0
    totalArea = 0
    pointCount = 0
    for i in range(0, 60, 1):
        animate(i, th)
    p = (1.0*total/pointCount) / (1.0*circleCount/totalArea)
    result_x.append(th)
    result_y.append(p)
    result_points.append(total)
    print(f"points count={total}, r={th}, p={p}")

fig = plt.figure()
host = fig.add_subplot(111)

par1 = host.twinx()

host.set_xlim(0, max_radius)

host.set_xlabel("Radius")
host.set_ylabel("Correlation")
par1.set_ylabel("# of Captured Points")

color1 = plt.cm.viridis(0)
color2 = plt.cm.viridis(0.5)

p1, = host.plot(result_x, result_y, color=color1,label="Correlation")
p2, = par1.plot(result_x, result_points, color=color2, label="# of Captured Points")

lns = [p1, p2]
host.legend(handles=lns, loc='best')

plt.show()
"""plt.plot(result_x, result_y, label="correlation")
plt.plot(result_x, result_points, label="# of points")
plt.show()"""
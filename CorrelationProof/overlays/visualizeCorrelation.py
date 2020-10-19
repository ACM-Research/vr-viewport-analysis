from typing import List

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

from overlay import DataParser
#
#
# THRES = 500
# vid_id = 24 # TODO
#
#
# def pointsToXY(points):
#     x_list = [x for [x, y] in points]
#     y_list = [y for [x, y] in points]
#     return x_list, y_list
#
# def dist(p1, p2):
#     return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
#
# def animate(f, *fargs):
#     global ij, total, img, vid_id, circleCount, totalArea, pointCount
#
#     # graph salient points
#     points = data[f]["salient"]
#     graph.set_data(pointsToXY(points))
#
#     #show image
#     im = Image.open(f"Experiment Data/SampleVideos/SourceFrames/{vid_id}/frame{ij * 30 + 1}.jpg")  # .transpose(Image.FLIP_TOP_BOTTOM)
#     if img is None:
#         img = axes[0].imshow(im)
#     else:
#        img.set_data(im)
#
#     # remove circles from last animation frame
#     for obj in axes[0].findobj(match=type(plt.Circle(1, 1))):
#         obj.remove()
#
#     # draw circles for this frame
#     for salient in points:
#         circle1 = plt.Circle((salient[0], salient[1]), THRES, color='r', fill=False)
#         axes[0].add_artist(circle1)
#
#     # process trace points into:
#     # 1. inRangePoints:  points inside of at least one salient feature's threshold radius
#     # 2. outRangePoints: points not inside any salient feature's threshold radius
#     points2 = data[f]["trace"]
#     inRangePoints = []
#     outRangePoints = []
#     for p in points2:
#         found = False
#         for j in points:
#             if dist(p, j) < THRES * THRES:
#                 found = True
#                 break
#         if found:
#             inRangePoints.append(p)
#         else:
#             outRangePoints.append(p)
#
#     # keep track of statistics
#     p = len(inRangePoints) / len(points2) * 100
#     line.append(p)
#     ij += 1
#     total += len(inRangePoints)
#     pointCount += len(points2)
#     circleArea = len(points)*3.14*THRES*THRES / 1920000
#     totalArea += circleArea
#     circleCount += len(points)
#     #print("Average: " + str(total / ij)+ ", " + str(circleArea))
#     print( (1.0*total/pointCount) / (1.0*totalArea/circleCount))
#     # display points for image subplot
#     in_range.set_data(pointsToXY(inRangePoints))
#     others.set_data(pointsToXY(outRangePoints))
#
#     # display chart for percentage of points covered in threshold
#     axes[1].cla()
#     axes[1].plot(np.arange(ij), line)
#
#     return graph, in_range, others

#
# # read in vid 24's data
# data = []
# with open("CorrelationProof/overlays/data.txt", 'r') as f:
#     data = json.load(f)
#
# # setup subplots and init image subplot
# fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 7))
# axes[0].set_xlim([0, 3840])
# axes[0].set_ylim([1920, 0])
# fig.tight_layout()
#
# # setup the three types of points for image subplot
# graph, = axes[0].plot([], [], 'o')
# in_range, = axes[0].plot([], [], 'o')
# others, = axes[0].plot([], [], 'o')
#
# ij = 0
# line = []
# total = 0
# img = None
# circleCount = 0
# totalArea = 0
# pointCount = 0
#
#
# # animation (59 goes up to 59 * 30 + 1 = 1771'th frame)
# ani = FuncAnimation(fig, animate, frames=59, interval=500, repeat=False)
#
# # uncomment to save (alternate comment with plt.show())
# # ani.save('CorrelationProof/overlays/demo.gif', writer='imagemagick', fps=3)
#
# # show animation (alternate comment with ani.save())
# plt.show()
# print(1.0*totalArea/circleCount)
# print(1.0*total/ij)
#


class CorrelationVisualizer:
    data: DataParser
    predicate: DataParser.Predicate
    thres: int
    # Animation variables
    ij: int
    line: List[float]
    total: int
    img: Image
    circleCount: int
    totalArea: int
    pointCount: int

    # The animation class itself
    ani: FuncAnimation

    # Auxilliary variables related to plotting and animation
    fig: Figure
    axes: Axes

    graph: Line2D
    in_range: Line2D
    others: Line2D

    def __init__(self, data: DataParser, threshold: int, pred: DataParser.Predicate = None):
        self.data = data
        self.thres = threshold
        self.predicate = pred

        # setup subplots and init image subplot
        self.fig, self.axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 7))
        self.axes[0].set_xlim([0, 3840])  # TODO: Make these not constants
        self.axes[0].set_ylim([1920, 0])
        self.fig.tight_layout()

        # setup the three types of points for image subplot
        self.graph, = self.axes[0].plot([], [], 'o')
        self.in_range, = self.axes[0].plot([], [], 'o')
        self.others, = self.axes[0].plot([], [], 'o')

        # some variables to keep track of statistics
        self.ij = 0
        self.line = []
        self.total = 0
        self.img = None
        self.circleCount = 0
        self.totalArea = 0
        self.pointCount = 0

    @staticmethod
    def animate(frameindex, *fargs):
        # "self" is passed back through fargs
        self: CorrelationVisualizer = fargs[0]

        # graph salient points
        # points = data[frameindex]["salient"]

        points = []
        # Inefficent and lazy TBH
        for feature in self.data.salparser.features:
            if None not in feature.positions[frameindex * 30 + 1]:
                points.append(feature.positions[frameindex * 30 + 1])
        self.graph.set_data(self.pointstoxy(points))

        # show image
        im = Image.open(
            f"Experiment Data/SampleVideos/SourceFrames/{self.data.vidid}/frame{self.ij * 30 + 1}.jpg")
        #   # .transpose(Image.FLIP_TOP_BOTTOM)
        if self.img is None:
            self.img = self.axes[0].imshow(im)
        else:
            self.img.set_data(im)

        # remove circles from last animation frame
        for obj in self.axes[0].findobj(match=type(plt.Circle((1.0, 1.0)))):
            obj.remove()

        # draw circles for this frame
        for salient in points:
            circle1 = plt.Circle((salient[0], salient[1]), self.thres, color='r', fill=False)
            self.axes[0].add_artist(circle1)

        # process trace points into:
        # 1. inRangePoints:  points inside of at least one salient feature's threshold radius
        # 2. outRangePoints: points not inside any salient feature's threshold radius

        # points2 = data[f]["trace"]
        # Strip out user ID and frame
        points2 = [trace[2] for trace in
                   self.data.usertraces_with_predicate(self.data.quesparser, self.predicate, frameindex * 30 + 1)]
        in_range_points = []
        out_range_points = []
        for p in points2:
            found = False
            for j in points:
                if self.dist(p, j) < self.thres * self.thres:
                    found = True
                    break
            if found:
                in_range_points.append(p)
            else:
                out_range_points.append(p)

        # keep track of statistics
        p = len(in_range_points) / len(points2) * 100
        self.line.append(p)
        self.ij += 1
        self.total += len(in_range_points)
        self.pointCount += len(points2)
        self.circleArea = len(points) * 3.14 * self.thres * self.thres / 1920000
        self.totalArea += self.circleArea
        self.circleCount += len(points)
        # print("Average: " + str(total / ij)+ ", " + str(circleArea))
        print((1.0 * self.total / self.pointCount) / (1.0 * self.totalArea / self.circleCount))
        # display points for image subplot
        self.in_range.set_data(self.pointstoxy(in_range_points))
        self.others.set_data(self.pointstoxy(out_range_points))

        # display chart for percentage of points covered in threshold
        self.axes[1].cla()
        self.axes[1].plot(np.arange(self.ij), self.line)

        return self.graph, self.in_range, self.others

    def render(self):
        # animation (59 goes up to 59 * 30 + 1 = 1771'th frame)
        self.ani = FuncAnimation(self.fig, self.animate, frames=59, interval=500, repeat=False, fargs=(self,))

        # uncomment to save (alternate comment with plt.show())
        # ani.save('CorrelationProof/overlays/demo.gif', writer='imagemagick', fps=3)

        # show animation (alternate comment with ani.save())
        plt.show()
        print(1.0 * self.totalArea / self.circleCount)
        print(1.0 * self.total / self.ij)

    @staticmethod
    def pointstoxy(points):
        x_list = [x for [x, _] in points]
        y_list = [y for [_, y] in points]
        return x_list, y_list

    @staticmethod
    def dist(p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def main():
    from overlay import sample_predicate
    data = DataParser(24, "C:/Users/qwe/Documents/vr-viewport-analysis")
    data.generatedata()
    renderer = CorrelationVisualizer(data, 500, sample_predicate)
    renderer.render()


if __name__ == "__main__":
    main()

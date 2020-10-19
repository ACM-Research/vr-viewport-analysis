from typing import Tuple, List, Dict, Callable

import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math
import json

from QuestionnaireParser import QuestionnaireParser, Questionnaire
from vidToFrames import FrameGenerator
from SalientFeatureParser import SalientFeatureParser, SalientFeaturePosition

import os
print(os.getcwd())


def sample_exclusion_fxn(predicate: str, questionnaire: QuestionnaireParser) -> bool:
    """This family of functions dictates how users should be excluded from the process
    based on their answers from the background questionnaire."""
    #return questionnaire.participants[predicate].mobilevr >= 2
    return True


class Frame:
    sal_points: int
    vp_traces: int
    width: int
    height: int

    def __init__(self, salpts, vptraces, width, height):
        self.sal_points = salpts
        self.vp_traces = vptraces
        self.width = width
        self.height = height


class DataParser:
    # Single trace: the user ID, the frame it was on, and the position projected to 2D
    UserTrace = Tuple[str, int, Tuple[float, float]]
    # Predicate function for exclusion of user traces based on background questionnaire
    Predicate = Callable[[QuestionnaireParser, UserTrace], bool]

    salparser: SalientFeatureParser
    quesparser: QuestionnaireParser
    usertraces: List[UserTrace]
    basedir: str
    vidid: int
    questionnairepath: str
    frames: Dict[int, Frame]
    imagesize: Tuple[int, int]
    
    def __init__(self, vidid: int, basedir: str):
        """This constructor only initializes the cheap things to construct.
        The expensive operation generatedata() calls all the expensive functions."""
        self.vidid = vidid
        self.basedir = basedir
        self.questionnairepath = f"{basedir}/Experiment Data/Questionnaires/BackgroundQuestionnaire.csv"
        self.salienttracepath = f"{basedir}/Finished POI Spreadsheets/{self.vidid} POI Finished.xlsx"
        self.usertracepath = f"{basedir}/CorrelationProof/overlays/GroupByVideos/{self.vidid}"
        # Format string this with the % method for frame.
        self.imagepath = f"{basedir}/Experiment Data/SampleVideos/SourceFrames/{self.vidid}/frame%d.jpg"

        self.frames = {}
        # Cheap to construct- the image isn't actually parsed with Image.open, it's a lazy fxn
        with Image.open(self.imagepath % 1) as im:
            self.imagesize = (im.size[0], im.size[1])

    @staticmethod
    def convvec2angl(vector):
        phi = math.degrees(math.asin(vector[1]))
        theta = math.degrees(math.atan2(vector[0], vector[2]))
        return theta, phi

    def initparsers(self):
        self.quesparser = QuestionnaireParser(self.questionnairepath)
        self.salparser = SalientFeatureParser(self.salienttracepath)

    def generateframes(self):
        """Generate frames on demand."""
        FrameGenerator(self.vidid, self.salparser.features[0]).generateframes()

    def importusertraces(self):
        """Note that this parser is very simple in nature and doesn't really *need*
        a separate class."""
        all_user_traces = []
        user_folders = [trace for trace in os.listdir(self.usertracepath)]
        for user in user_folders:
            # Test for exclusion.
            # Or we would, if it weren't now done at runtime.
            # if QuestionnaireParser is not None:
            #     if not sample_exclusion_fxn(user[: user.find('.csv')], self.quesparser):
            #         continue
            userid = user[: user.find('.csv')]
            trace_data = pd.read_csv(f"{self.usertracepath}/{user}")
            trace_rows = trace_data.values
            all_user_traces.append((trace_rows, userid))

        self.convertusertraces(all_user_traces)

    def convertusertraces(self, unparsed_user_traces):
        # draw user trace points
        self.usertraces = []
        for trace_rows, userid in unparsed_user_traces:
            for frame in self.salparser.frameList:
                trace_row = trace_rows[frame - 1]  # Be careful about indexing!!
                arr = [trace_row[5], trace_row[6], trace_row[7]]
                x, y = self.convvec2angl(arr)
                x = ((x+180)/360) * self.imagesize[0]
                y = ((90-y)/180) * self.imagesize[1]
                self.usertraces.append((userid, frame, (x, y)))

    def generatedata(self):
        self.initparsers()
        self.generateframes()
        self.importusertraces()

    def usertraces_with_predicate(self, q: QuestionnaireParser, pred: Predicate = None):
        """A generator function that takes the imported User Trace data and yields
        the next Trace that matches the predicate pred."""
        for trace in self.usertraces:
            if pred is None:
                yield trace
            elif pred(q, trace):
                yield trace


class OverlayPlayer:
    pauseinterval: int
    salientcolor: str
    tracecolor: str
    data: DataParser

    def __init__(self, parser: DataParser, pred: DataParser.Predicate = None):
        self.data = parser
        self.salientcolor = 'r'
        self.tracecolor = 'g'
        self.pauseinterval = 0.5
        self.predicate = pred

    def render(self):
        for frame in self.data.salparser.frameList:
            self.renderframe(frame)
            plt.pause(self.pauseinterval)
            plt.draw()

    def renderframe(self, frame: int):
        # Some salient feature traces may have an extra frame attached that doesn't exist.
        # Cleanly ignore that frame if it doesn't exist.
        try:
            im = Image.open(self.data.imagepath % frame)
        except FileNotFoundError:
            return
        # TODO: Rewrite this using object-oriented pyplot
        img = plt.imshow(im)

        # Remove the plots from the previous frame.
        [p.remove() for p in reversed(plt.gca().patches)]

        # Render new Salient Features.
        for feature in self.data.salparser.features:
            if None not in feature.positions[frame]:
                self.renderrectangle(plt, feature.positions[frame], self.salientcolor)

        # Render new User Traces.
        for trace in self.data.usertraces_with_predicate(self.data.quesparser, self.predicate):
            # This part is probably super inefficient
            if trace[1] != frame:
                continue

            self.renderrectangle(plt, trace[2], self.tracecolor)

    def renderrectangle(self, plotter, pos: Tuple[int, int], color: str):
        rect = patches.Rectangle(pos, 60, 60, linewidth=3, edgecolor=color, facecolor='none')
        plotter.gca().add_patch(rect)


def play_video(vid_id: str, questionnaire: QuestionnaireParser = None, draw=True):
    img = None

    poi_data = SalientFeatureParser(f'Finished POI Spreadsheets/{vid_id} POI Finished.xlsx')


    trace_rows_all = []
    user_folders = [trace for trace in os.listdir(f'CorrelationProof/overlays/GroupByVideos/{vid_id}')]
    for user in user_folders:
        # Test for exclusion.
        if QuestionnaireParser is not None:
            if not sample_exclusion_fxn(user[: user.find('.csv')], questionnaire):
                continue
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

    process_data = []
    for frame in poi_data.frameList:
        print(frame)

        # get frame
        if draw:
            im = Image.open(f'Experiment Data/SampleVideos/SourceFrames/{vid_id}/frame{frame}.jpg')
            im_size0 = im.size[0]
            im_size1 = im.size[1]
            if img is None:
                img = plt.imshow(im)
            else:
                img.set_data(im)

        # draw manually selected salient features
        # frame = row[0]
        remove_patches(plt, draw)
        for feature in poi_data.features:
            salient_points = draw_patches(plt, feature, frame, draw)

        # draw user trace points
        all_user_points = []
        for trace_rows in trace_rows_all:
            trace_row = trace_rows[frame - 1]  # Indexing!
            arr = [trace_row[5], trace_row[6], trace_row[7]]
            x, y = convvec2angl(arr)
            x = ((x+180)/360)*im_size0
            y = ((90-y)/180)*im_size1
            all_user_points.append((x, y))
            if draw:
                draw_rectangle(plt, (x, y), 'g')

        # add to output data
        process_data.append({'index': frame, 'salient': salient_points, 'trace': all_user_points, 'width': im_size0, 'height': im_size1})

        # redraw
        if draw:
            plt.pause(1)
            plt.draw()

    return process_data


def remove_patches(plotter, draw=True):
    if draw:
        [p.remove() for p in reversed(plotter.gca().patches)]


def draw_patches(plotter, feature: SalientFeaturePosition, frame: int, draw=True):
    salient_points = []
    if draw:
        if None not in feature.positions[frame]:
            draw_rectangle(plotter, feature.positions[frame], 'r')
    return salient_points


def draw_rectangle(plotter, pos: Tuple[int, int], color):
    rect = patches.Rectangle(pos, 60, 60, linewidth=3, edgecolor=color, facecolor='none')
    plotter.gca().add_patch(rect)


def sample_predicate(q: QuestionnaireParser, trace: DataParser.UserTrace) -> bool:
    return q.participants[trace[0]].mobilevr >= 2


def main():
    # vid_id = 24
    # quesparser = QuestionnaireParser()
    # data = play_video(vid_id, questionnaire=quesparser, draw=True)
    # Change False to True to show overlay
    # However, False will run a lot faster (for outputting data file)
    # with open("CorrelationProof/overlays/data.txt", 'w') as f:
    #     json.dump(data, f)
    data = DataParser(24, "C:/Users/qwe/Documents/vr-viewport-analysis")
    data.generatedata()
    renderer = OverlayPlayer(data, sample_predicate)
    renderer.render()


if __name__ == "__main__":
    main()

from typing import Tuple, List, Dict

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
    return questionnaire.participants[predicate].mobilevr >= 2


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
    salparser: SalientFeatureParser
    quesparser: QuestionnaireParser
    # List of a single trace: the user ID, the frame it was on, and the position projected to 2D
    usertraces: List[Tuple[str, int, Tuple[float, float]]]
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
        self.questionnairepath = "/Experiment Data/Quesionnaires/BackgroundQuestionnaire.csv"
        self.salienttracepath = f"/Finished POI Spreadsheets/{self.vidid} POI Finished.xlsx"
        self.usertracepath = f"CorrelationProof/overlays/GroupByVideos/{self.vidid}"
        # Format string this with the % method for frame.
        self.imagepath = f"Experiment Data/SampleVideos/SourceFrames/{self.vidid}/frame%d.jpg"

        self.frames = {}
        # Cheap to construct- the image isn't actually parsed with Image.open, it's a lazy fxn
        with Image.open(self.imagepath % 1) as im:
            self.imagesize = (im.size[0], im.size[1])

    def initparsers(self):
        self.quesparser = QuestionnaireParser(self.basedir + self.questionnairepath)
        self.salparser = SalientFeatureParser(self.salienttracepath)

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
                trace_row = trace_rows[frame]
                arr = [trace_row[5], trace_row[6], trace_row[7]]
                x, y = convvec2angl(arr)
                x = ((x+180)/360) * self.imagesize[0]
                y = ((90-y)/180) * self.imagesize[1]
                self.usertraces.append((userid, frame, (x, y)))

    def generatedata(self):
        self.initparsers()
        self.importusertraces()


class OverlayPlayer:
    data: DataParser

    def __init__(self, parser: DataParser):
        self.data = parser

    def renderframe(self, frame: int):
        pass


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


def convvec2angl(vector):
    phi = math.degrees(math.asin(vector[1]))
    theta = math.degrees(math.atan2(vector[0], vector[2]))
    return theta, phi


def main():
    vid_id = 24
    quesparser = QuestionnaireParser()
    # Generate frames as needed.
    # FrameGenerator(vid_id, salparser.features[0]).generateframes()
    # Change False to True to show overlay
    # However, False will run a lot faster (for outputting data file)
    data = play_video(vid_id, questionnaire=quesparser, draw=True)
    with open("CorrelationProof/overlays/data.txt", 'w') as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()

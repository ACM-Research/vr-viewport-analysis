"""Note to self...
A better optimization would be to deliver frames on demand
and spin off a task to flush that frame to disk."""
from typing import List, Optional

import cv2
import os
from SalientFeatureParser import SalientFeaturePosition


class FrameGenerator:
    requestedFrames: Optional[List[int]]
    cap: cv2.cv2.VideoCapture
    vid_id: int

    def __init__(self, basedir: str, vidid: int, framerequest: SalientFeaturePosition = None):
        self.vid_id = vidid
        self.videoPath = f'{basedir}/Experiment Data/SampleVideos/Source/{self.vid_id}.mp4'
        self.framesPath = f'{basedir}/Experiment Data/SampleVideos/SourceFrames/{self.vid_id}'
        self.cap = cv2.VideoCapture(self.videoPath)

        self.requestedFrames = list(framerequest.positions.keys()) if framerequest is not None else None

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def checkframelist(self):
        """Double checks requestedFrames against the list of frames actually
        generated. Note that you MUST call this for certain videos!
        Certain Salient Traces will request frames that don't actually exist.
        This cannot be called in the constructor, because frames may have not yet
        been generated. Make sure you call generateframes() first."""
        for index, frame in enumerate(self.requestedFrames):
            if not os.path.exists(self.framesPath):
                raise Exception("Cannot double check frames if frames have not been generated!")

            path = f"{self.framesPath}/frame{frame}.jpg"
            if not os.path.exists(path):
                del self.requestedFrames[index]

    def generateframes(self):
        """Generates frames for videos as needed. Will not
        generate frames if they've already been generated."""
        # Caching mechanism- don't generate if frames were already rendered
        if os.path.exists(self.framesPath):
            return
        print(f"Generating frames for video {self.vid_id}")
        if self.requestedFrames is not None:
            print(f"Frames requested: {self.requestedFrames}")
        self.mkdir(self.framesPath)
        count = 0
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            # This cleanly exits if we can't grab another frame
            if not ret:
                break
            cond = count in self.requestedFrames if self.requestedFrames is not None else count % 30 == 1
            if cond:
                outpath = f"{self.framesPath}/frame{count}.jpg"
                cv2.imwrite(outpath, frame)
                print(f"Frame {outpath} written to disk")
            count += 1

    @staticmethod
    def mkdir(directory: str):
        if not os.path.exists(directory):
            os.makedirs(directory)

"""Note to self...
A better optimization would be to deliver frames on demand
and spin off a task to flush that frame to disk."""






import cv2
import os
from CorrelationProof.overlays.SalientFeatureParser import SalientFeaturePosition


class FrameGenerator:
    cap: cv2.cv2.VideoCapture
    vid_id: int

    def __init__(self, vidid: int, framerequest: SalientFeaturePosition = None):
        self.vid_id = vidid
        self.videoPath = f'Experiment Data/SampleVideos/Source/{self.vid_id}.mp4'
        self.framesPath = f"Experiment Data/SampleVideos/SourceFrames/{self.vid_id}"
        self.cap = cv2.VideoCapture(self.videoPath)

        self.requestedFrames = framerequest.positions.keys() if framerequest is not None else None

    def __del__(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def generateframes(self):
        # Caching mechanism- don't generate if frames were already rendered
        if os.path.exists(self.framesPath):
            return
        self.mkdir(self.framesPath)
        count = 0
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            # This cleanly exits if we can't grab another frame
            if not ret:
                break
            cond = count in self.requestedFrames if self.requestedFrames is not None else count % 30 == 1
            if cond:
                cv2.imwrite(f"{self.framesPath}/frame{count}.jpg", frame)
            count += 1

    @staticmethod
    def mkdir(directory: str):
        if not os.path.exists(directory):
            os.makedirs(directory)

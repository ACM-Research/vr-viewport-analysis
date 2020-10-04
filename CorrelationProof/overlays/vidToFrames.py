import cv2
import os


def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


vid_id = 24
cap = cv2.VideoCapture(f'Experiment Data/SampleVideos/Source/{vid_id}.mp4')
mkdir("Experiment Data/SampleVideos/SourceFrames/{vid_id}")

count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if count % 30 == 1:
        cv2.imwrite(f"Experiment Data/SampleVideos/SourceFrames/{vid_id}/frame{count}.jpg", frame)
    count = count + 1

cap.release()
cv2.destroyAllWindows()

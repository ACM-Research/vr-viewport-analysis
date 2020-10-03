import cv2
cap = cv2.VideoCapture('../Experiment Data/SampleVideos/Source/23.mp4')
count = 0
while cap.isOpened():
    ret,frame = cap.read()
    if count % 30 == 1:
        cv2.imwrite("../Experiment Data/SampleVideos/SourceFrames/23/frame%d.jpg" % count, frame)
    count = count + 1

cap.release()
cv2.destroyAllWindows()
import numpy as np
import cv2
import json

from matplotlib import pyplot as plt
# point is to add keypoints to a json that is easily parsable 
# 
def addKeyPoints():
    i = 1
    img = cv2.imread(f"Experiment Data/SampleVideos/SourceFrames/23/frame1.jpg", 0)

    while True:
        # Trying to dump this into a json file called newPOI.json -> index = {}
        # Initiate ORB detector
        orb = cv2.ORB_create()

        # find the keypoints with ORB
        kp = orb.detect(img, None)

        # Not too sure about this, needs fixing later 
        with open("newPOI.json", "w") as fp:
            json.dump([{"Points": point.pt} for point in kp], fp, indent=4)

        # compute the descriptors with ORB
        kp, des = orb.compute(img, kp)

        # draw only keypoints location,not size and orientation
        img2 = cv2.drawKeypoints(img,kp,color=(0,255,0), flags=0, outImage=img)
        plt.imshow(img2),plt.show()

        # waits 100ms in order for a key, if esc is pressed the program exits
        ch = cv2.waitKey(100)
        if ch == 27: 
            break
        cv2.waitKey(100)
        
        # read another image
        img = cv2.imread(f"Experiment Data/SampleVideos/SourceFrames/23/frame{i * 30 + 1}.jpg", 0)
        i += 1

        
def main():
    addKeyPoints()

if __name__ == "__main__":
    main()

cv2.destroyAllWindows()
cv2.waitKey(1)
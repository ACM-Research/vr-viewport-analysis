# Overlay

## Information

To prove that there is a correlation, it might be easier to first observe users' viewports and salient features overlayed onto the video. To help us do that, there are two scripts in this folder:

`vidToFrames.py` is a helper script that uses OpenCV to turn `.mp4` files into frames (every 30 frames). It reads in a video from `Experiment Data/SampleVideos/Source/VIDEO_ID.mp4` and outputs the frames into `Experiment Data/SampleVideos/SourceFrames/VIDEO_ID`. Although there are frames available in the `Salient Feature Traces/` folder, those have grids overlayed on them and are not full resolution.

`overlay.py` overlays both user viewports (from `Experiment Data/Traces/USER_ID/`) and salient feature information (from `Salient Feature Traces/VIDEO_ID/POI.xlsx`) onto the video frames (stored in `Experiment Data/SampleVideos/SourceFrames/VIDEO_ID` by `vidToFrames.py`). This enables us to visualize the user's viewport through each individual frame of the videos. The script also outputs `data.txt`, which contains a list of frames with their corresponding salient feature and user viewport traces.

`groupTraceByVid.py` groups Traces by video ID rather than user ID. Results are stored in `CorrelationProof/overlays/GroupByVideos` (might consider moving to experiment data instead?)

`visualizeCorrelation.py` shows a visualization of different threshold radius values. In the demo, there are two subplots. The first shows the image with salient features and traces overlayed (with circles of radius `THRESHOLD`) to show which points are inside of the threshold value. The bottom chart shows the percentage of points that are included by at least one of the circles. In the console, the average number of points is also being printed out for testing.

![demo](demo.gif)

## Technical Implementation

`vidToFrames.py` uses OpenCV to read frame by frame and write every 30 frames.

`overlay.py` uses conversion algorithms from the MATLAB scripts (`overlay.m`) to convert users' viewport quaternions into `(x,y)` coordinates. 

## How to Run

1. Install the necessary dependencies (located at `CorrelationProof/requirements.txt`): `pip install -r requirements.txt`
2. Run: `python overlay.py`
3. To generate frames folder for a video, modify `vidToFrames.py` appropriately and run `python vidToFrames.py`
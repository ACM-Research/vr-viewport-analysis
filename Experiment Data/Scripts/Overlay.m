%This scripts creates the overlaid video for an input video from viewport
%traces in the dataset
%INPUTs section should be set according to the desired video input

%% INPUTs
%video ID, according to videoID in the paper, to load viewport traces for this video
vidID=19;

%startTime Offset of video in seconds: according to time offsets in Table 1
%in the paper; Example 1:40 -> 100
timeOffset=0;

%path to source video: It should be in equirectangular projection
srcVidPath=['..\SampleVideos\Source\',num2str(vidID),'.mp4'];

%path to output video
dstVidPath=[num2str(vidID),'.avi'];

%path to viewport traces in the dataset
tracePath='..\Traces\';


%% Parameters
%output video size
outWidth=1920/4;
outHeight=1080/4;
%kernel for viewport center
kern=fspecial('gaussian',ceil(outWidth*(10/360)),2);

%% Load video
v=VideoReader(srcVidPath);

videoWriter = VideoWriter(dstVidPath);
videoWriter.FrameRate=v.FrameRate;
videoWriter.Quality=100;
open(videoWriter);


%seek to video start
v.CurrentTime=timeOffset;


%set rotation based on videoID, some videos were reoriented for playback
rotation=0;
if vidID==10
    rotation=-95;
elseif vidID==17
    rotation=180;
elseif vidID==27
    rotation=63;
elseif vidID==28
    rotation=81;
end




%% load viewport traces for this video

viewer=cell(30);
idx=1;
files = dir(tracePath);
directoryNames = {files([files.isdir]).name};
directoryNames = directoryNames(~ismember(directoryNames,{'.','..'}));
for fol= directoryNames
    fileName=strcat(tracePath,char(fol),'/',char(fol),'_',num2str(vidID),'.csv');
    if ~exist(fileName,'file')
        continue;
    end
    viewer{idx}=importdata(fileName);
    idx=idx+1;
end



%% for each frame of the video: reorient, and apply overlay layer
for StartTime=0:1/(v.FrameRate):60
    if(v.hasFrame)
     f=readFrame(v);
    else
     break;
    end

    %% reorient the video if it is rotated
    w=v.Width;
    if rotation~=0
       newF=zeros(size(f,1),size(f,2),size(f,3),'uint8');
       if  rotation>0
           x=floor((rotation/360)*w);
           newF(:,1:x,:)=f(:,w-x+1:w,:);
           newF(:,x+1:w,:)=f(:,1:w-x,:);
       elseif rotation<0
           x=floor((-rotation/360)*w);
           newF(:,w-x+1:w,:)=f(:,1:x,:);
           newF(:,1:w-x,:)=f(:,x+1:w,:);
       end
       f=newF;
       clear newF;
    end

    f=imresize(f,[outHeight,outWidth]);
    imshow(f);
    hold on

    %% Apply overlay of viewports
    num=0;
    map=zeros(outHeight, outWidth);
    for idx=1: 30

        data=viewer{idx};
        num=num+1; 
        i=1;
        while(i<size(data,1) && data(i,1)<StartTime)
            i=i+1;
        end
        %for each view
        currMap=zeros(outHeight, outWidth);
        [x,y]=ConvVec2Angl(data(i,6:8));
        currMap=mixMapKern(currMap,kern,x,y);
        i=i+1;
        map=currMap+map;
    end

    %
    map=map/num;
    imagesc(map);
    colormap hot
    hold off
    alpha(0.5);
    fr=getframe(gcf);
    fr=fr.cdata;
    writeVideo(videoWriter,fr);
end

close(videoWriter);

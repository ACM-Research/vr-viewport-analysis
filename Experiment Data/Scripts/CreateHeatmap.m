%this script creates a heatmap of viewport centers on a single frame of a video

%INPUTS
%path to trace folders
path='../traces/';
%path to video files
videoPath= '../videos/';


width=1920/4;  %output width
height=1080/4; %output height
    
%video ID
vidID=1;

%video start time for creating heatmap
StartTime=0;
%video end time for heatmap creation
EndTime=0.5;

%end of INPUTS

%kernel
kern=fspecial('gaussian',ceil(width*(10/360)),2);

files = dir(path);
directoryNames = {files([files.isdir]).name};
directoryNames = directoryNames(~ismember(directoryNames,{'.','..'}));

v=VideoReader(strcat(videoPath,num2str(vidID),'.mp4'));
if(v.hasFrame)
    f=readFrame(v);
end

f=imresize(f,[height,width]);
imshow(f);
map=zeros(height, width);
for StartTime=0:1/(v.FrameRate):EndTime
    num=0;
    hold on
    currMap=zeros(height, width);
    for fol= directoryNames
        fileName=strcat(path,char(fol),'/',char(fol),'_',num2str(vidID),'.csv');
        if ~exist(fileName,'file')
            continue;
        end
        num=num+1;
        %import data
        data=importdata(fileName);
        i=1;
        %seek to startTime
        while(i<size(data,1) && data(i,2)<StartTime)
            i=i+1;
        end
        
        %for each view
        [x,y]=ConvVec2Angl(data(i,6:8));
        currMap=mixMapKern(currMap,kern,x,y);
        i=i+1;
        map=currMap+map;
    end
    
    map=map/num;
end
imagesc(map);
colormap hot
hold off
alpha(0.5);

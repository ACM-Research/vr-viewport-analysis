%What does this script do?
%this script creates clusters for all videos
%the output is written in 'out' variable
%each row in out is for a video
%   the first column is average number of clusters
%   the second column is std. dev. for number of clusters
%   the third column is average number of viewers in the largest cluster
%   the fourgh column is std. dev. for average number of viewers in the largest clustet

%How to run
%to run this script you need to download Rossi et al, code from: https://github.com/LASP-UCL/spherical-clustering-in-VR-content
%copy this script and 'Myspherical_clustering.m' file to the downloaded folder and run this script

%path to trace files
path='../traces/';

%add folders for clustering algorithm
addpath('Data_input/')
addpath('Functions/')
addpath('Results/')


for vidID=1:30
    
    if(vidID==15 || vidID==16)
        continue;
    end
clc
clearvars -except vidID ff path


%sample rate
ff=30;
INTERVAL=1/ff;
StartTime=0;
EndTime=70;

files = dir(path);
directoryNames = {files([files.isdir]).name};
directoryNames = directoryNames(~ismember(directoryNames,{'.','..'}));

i=1;
for fol= directoryNames
    
    fileName=strcat(path,char(fol),'/',char(fol),'_',num2str(vidID),'.csv');
    if ~exist(fileName,'file')
        continue;
    end

    %import data
    out=importdata(fileName);
    %out(:,2)=out(:,2)-out(1,2);
    data=0;
    data=Bucketize(out,INTERVAL);
    Traj(i).data=data(:,6:8);
    Traj(i).data(ff*60+1:end,:)=[];
    if(length(Traj(i).data(:,1))<ff*60)
        temp=repmat(Traj(i).data(end,:),ff*60-length(Traj(i).data(:,1)),1);
        Traj(i).data=[Traj(i).data;temp];
    end
    i=i+1;
end

geod_dist_th = pi/5;
D = 1.8;    %sec
frame_rate = ff;
D = D*frame_rate;   %in n. frames

n_users = size(Traj,2);
n_frames = ff*60;


%ch_length = 1;
%D=1;
ch_length = ff*3;
clustering_rate = 1;        %input('Clustering rate ? [frames - 30 = 1sec] ')            %15;
ch = 1:ch_length:n_frames;  

for i_ch = 1:length(ch)
    
    name = sprintf('Ch_%d',i_ch);
    start_fr = ch(i_ch);
    selected_frames = start_fr:clustering_rate:start_fr+ch_length;
    selected_frames = selected_frames(1:end-1);
    
    
    for i_u = 1:n_users
        temp = Traj(i_u).data;
        Traj_temp(i_u,:).data = [temp(selected_frames,1) temp(selected_frames,2) temp(selected_frames,3)];
    end
    
    clique_clustersCh.(name) =  Myspherical_clustering(Traj_temp,geod_dist_th,D);
    
end


res=cell(20,1);
for i=1:20
    x=clique_clustersCh.(strcat('Ch_',num2str(i)));
    uni=unique(x);
    [result,e]=histcounts(x,length(uni));
    res{i}=result;
end

%store all cluster data in res_videoID.mat files
save(strcat('res_',num2str(vidID)),'res');


end

%extract average number of clusters, and average number of viewers in the
% largest cluster plus their standard deviation
K=30;
out=zeros(K,5);

for j=1:K
    if(j==15 || j==16)
        continue;
    end
t=load(strcat('res_',num2str(j),'.mat'));

res=0;m=0;
for i=1:length(t.res)
    
   res(i)=length(t.res{i});
   m(i)=t.res{i}(1);
end

out(j,:)=[mean(res) std(res) mean(m) std(m)];
end

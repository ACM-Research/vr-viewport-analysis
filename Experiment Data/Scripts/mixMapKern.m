function [ map ] = mixMapKern( map,kern, x, y )
%MIXMAPKERN Summary of this function goes here
%   Detailed explanation goes here

x=((x+180)/360)*size(map,2);
y=((90-y)/180)*size(map,1);
s=size(kern,1);
for i=ceil(x-s/2):ceil(x+s/2)-1
    for j=ceil(y-s/2):ceil(y+s/2)-1
       if(j<1 || j>size(map,1))
           continue;
       end
       if(i<1)
           map(j,i+size(map,2))=map(j,i+size(map,2))+kern(ceil(j-y+s/2),ceil(i-x+s/2));
       elseif(i>size(map,2))
            map(j,i-size(map,2))=map(j,i-size(map,2))+kern(ceil(j-y+s/2),ceil(i-x+s/2));
       else
           map(j,i)=map(j,i)+kern(ceil(j-y+s/2),ceil(i-x+s/2));
       end
    end
end


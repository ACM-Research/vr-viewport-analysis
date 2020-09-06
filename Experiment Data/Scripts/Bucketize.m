function [ out ] = Bucketize( data ,interval)
%BUCKETIZE Summary of this function goes here
%   this function takes samples from input 'data' at fixed 'interval's
%   out is the sampled data
    j=1;
    i=1;
    out=data(1,:);
    while i<=size(data,1)
        out(j,:)=data(i,:);
        j=j+1;
        i=i+1;
        while(i<=size(data,1) && data(i,1)<=(j-1)*interval)
            i=i+1;
        end
    end

end


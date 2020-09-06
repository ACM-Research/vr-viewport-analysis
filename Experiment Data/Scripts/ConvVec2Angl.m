function [ theta, phi ] = ConvVec2Angl( vector )
%CONVVEC2ANGL Summary of this function goes here
%   This function converts input 'vector' to according to the paper coordinate system
%   theta is yaw between -180 to 180, and phi is pitch between -90 to 90
    [t,p,r]=cart2sph(vector(3),vector(1),vector(2));
    theta=rad2deg(t);
    phi=rad2deg(p);

end


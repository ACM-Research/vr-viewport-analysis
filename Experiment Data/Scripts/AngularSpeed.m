function [ omega ] = AngularSpeed( v1, v2, dt )
%ANGLSPEED Summary of this function goes here
%   v1 and v2 are vectors
%   dt is the delta time
%   if dt==1 the distance will be shown
%   omega is the output great-circle distance in radian

omega=acos(dot(v1/norm(v1),v2/norm(v2)))/dt;

end

function [Clustered_traj] = spherical_clustering(UsersTraj,geod_th,D)
%this has been changed from spherical_clustering used in "SPHERICAL CLUSTERING OF USERS NAVIGATING 360◦ CONTENT"
% clique clustering extended for trajectories
% presented in "SPHERICAL CLUSTERING OF USERS NAVIGATING 360◦ CONTENT"
%
% Author: s.rossi@ucl.ac.uk
%        F.De.Simone@cwi.nl
%        pascal.frossard@epfl.ch
%        l.toni@ucl.ac.uk
%
%Given a set of trajectories on the sphere this function clusterise the
%users based on the presented algorithm
n_frames = size(UsersTraj(1).data,1);
n_users = size(UsersTraj,1);

matrix_distance = zeros(n_users,n_users); %adjacienct matri

for i_frame = 1:n_frames
    pair_distance = zeros(n_users,n_users);
    for i = 1:n_users
        
        xyz_i = UsersTraj(i).data;
        xyz_i = xyz_i(i_frame,:);
        [theta_user_i,phi_user_i]=ConvVec2Angl(xyz_i);
        theta_user_i=deg2rad(theta_user_i);
        phi_user_i=deg2rad(phi_user_i);
        %phi_user_i = acos(xyz_i(3));
        %theta_user_i= atan2(xyz_i(2),xyz_i(1));
        
        for j = i+1: n_users
            
            xyz_j = UsersTraj(j).data;
            xyz_j = xyz_j(i_frame,:);
            
            [theta_user_j,phi_user_j]=ConvVec2Angl(xyz_j);
            theta_user_j=deg2rad(theta_user_j);
            phi_user_j=deg2rad(phi_user_j);
            %phi_user_j = acos(xyz_j(3));
            %theta_user_j= atan2(xyz_j(2),xyz_j(1));
            
            pair_distance(i,j) = distance(phi_user_i,theta_user_i,phi_user_j,theta_user_j, [1 0],'radians');
            pair_distance(j,i) = pair_distance(i,j);
            
        end
    end
    
    matrix_distance_temp = zeros(n_users,n_users);
    matrix_distance_temp(pair_distance < geod_th) = 1;
    %pair_distance(pair_distance ~= 1) = 0;
    matrix_distance = matrix_distance + matrix_distance_temp;

end

matrix_distance(matrix_distance < D) = 0;
matrix_distance(matrix_distance > 1) = 1;

[Clustered_traj] = clique_clustering(matrix_distance);

end


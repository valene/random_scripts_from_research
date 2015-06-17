#! /usr/bin/python
#module to identify and compare unique structures.

import sys, string, math, os, re,random
import scipy, numpy, numpy.linalg,scipy.linalg


def struct_unique(structlist):
	newstructlist = []
	uniquelist = []
	tol = 1e-4
	unflag = 0
	atommassdict ={"Li":6.94, "S":32.06, "X":19.82}
	#print structlist
	for i in range(len(structlist)):
		total_M = 1.0
		xcom = 0.0
		ycom = 0.0
		zcom = 0.0
		#calculate center of mass
		for j in range(len(structlist[i])):
		    #print string.split(structlist[i][j])[0]
                    total_M = total_M + atommassdict[string.split(structlist[i][j])[0]]
		    xcom = xcom + atommassdict[string.split(structlist[i][j])[0]] * float(string.split(structlist[i][j])[1]) 
		    ycom = ycom + atommassdict[string.split(structlist[i][j])[0]] * float(string.split(structlist[i][j])[2]) 
		    zcom = zcom + atommassdict[string.split(structlist[i][j])[0]] * float(string.split(structlist[i][j])[3]) 
                xcom = xcom/total_M
		ycom = ycom/total_M
		zcom = zcom/total_M
                #calculate inertial tensor
		inertia_tensor = numpy.zeros((3,3))
                for j in range(len(structlist[i])):
		    M = atommassdict[string.split(structlist[i][j])[0]] 
		    xc = float(string.split(structlist[i][j])[1])
		    yc = float(string.split(structlist[i][j])[2])
		    zc = float(string.split(structlist[i][j])[3])
		    clist = [xc, yc, zc]
		    rad2 = (xc - xcom)**2 + (yc - ycom)**2  + (zc -zcom)**2
		    iner = numpy.zeros((3,3))
		    for i0 in range(3):
			for j0 in range(3):
			    if i0 == j0 :
			       iner[i0, j0] = M*(rad2 - clist[i0]*clist[i0])
		            else :
			       iner[i0, j0] = -M*clist[i0]*clist[j0]	  
	            inertia_tensor = numpy.add(inertia_tensor,iner)
		#calculation of inertial tensor complete  
		#defining rotation matrix along principal axes
                eig_val,eig_vec = numpy.linalg.eig(inertia_tensor)
		idx = eig_val.argsort()[::-1]
                eig_val = eig_val[idx]
		eig_vec = eig_vec[:,idx]
		Rotmat = numpy.zeros((3,3))
		#the eigenvectors are column arranged.
		#Rotmat = vec_eig.transpose()
		#Rotmat = numpy.linalg.eig(inertia_tensor)[1].transpose()
                rot_struct = []
		for j in range(len(structlist[i])):
		    in_coord = []
		    full_coord = []
		    in_coord.append(string.split(structlist[i][j])[0])
                    coords = numpy.array([float(string.split(structlist[i][j])[1]),float(string.split(structlist[i][j])[2]),float(string.split(structlist[i][j])[3])])
		    coordr = numpy.dot(eig_vec,coords)
		    full_coord = in_coord + [coords[0] - xcom, coords[1] - ycom,  coords[2] - zcom, math.sqrt((coords[0] - xcom)**2 + (coords[1] - ycom)**2 + (coords[2] - zcom)**2)]
		    rot_struct.append(full_coord)
		    #rot_struct.append(numpy.array([string.split(structlist[i][j])[0],  coords[0], coords[1],  coords[2] , math.sqrt((coords[0] - xcom)**2 + (coords[1] - ycom)**2 + (coords[2] - zcom)**2)]))	
		#rearange the stucture in terms of distance from COM
		rot_struct.sort(key=lambda a :(a[4], a[0]))
		print '$$$$$$$$$$$$$$$$$$$$$$$$$$\n'
		print rot_struct
                newstructlist.append(rot_struct)
        #return newstructlist 
        for i in range(len(newstructlist)):
	        for j in range(len(newstructlist[i])):
		    dist = math.sqrt((newstructlist[i][j][1] - newstructlist[i][0][1])**2 + (newstructlist[i][j][2] - newstructlist[i][0][2])**2 + (newstructlist[i][j][3] - newstructlist[i][0][3])**2)
                    newstructlist[i][j].append(dist)
	#do another sort to to arrange according to distance from first atom.
	for i in newstructlist:
	    i.sort(key=lambda a: (a[4], a[0], a[5]))
	#iterate through newstructures with uniquestructures 
	#those that do not match, append to uniquestructures
	if newstructlist:
	   uniquelist.append(newstructlist[0])
	for i in range(len(newstructlist)):
	    for j in range(len(uniquelist)):
		    if len(newstructlist[i]) == len(uniquelist[j]):
			unflag = 0    
			for k in range(len(newstructlist[i])):
			    if str(newstructlist[i][k][0]) != str(uniquelist[j][k][0]) or abs(newstructlist[i][k][-1] - uniquelist[j][k][-1]) > tol  or abs(newstructlist[i][k][-2] - uniquelist[j][k][-2]) > tol:
			       unflag = unflag +1
			if unflag == 0:
			     break	
		    else:
			unflag = 1    
			continue  
	    if unflag != 0 :
		    uniquelist.append(newstructlist[i])

	return uniquelist
	#return newstructlist

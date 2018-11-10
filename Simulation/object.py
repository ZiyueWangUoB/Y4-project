#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 14:40:06 2018

@author: ziyuewang
"""
#This file is made for the objects, starting with base class and children
import numpy as np
import math
from pyquaternion import Quaternion


class objectType:
	#Alpha Beta Gamma are the tilts or angles to the x,y,z planes respectively.
    def __init__(self,material,alpha,beta,gamma,xPos,yPos,zPos,xProbeRange,yProbeRange):
        self.material = material
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.xPos = xPos
        self.yPos = yPos
        self.zPos = zPos
        self.xProbeRange = xProbeRange
        self.yProbeRange = yProbeRange
#Add future function here to calculate tilt, just stating variables for now
    #def findThickness(self)
    def findPlane(self,c1,c2,c3,c4): #This is generic for any plane
        vector12 = c2 - c1
        vector13 = c3 - c1
        n = np.cross(vector12,vector13)
        nNorm = n/np.linalg.norm(n)
        return nNorm, c1, c2, c3, c4            #Returns the normal vector alongside a point on that vector
    
    def findIntersectionThickness(self,planes,xProbePos,yProbePos):
        #To find the intersection, we break down the dot product algebra in order to rearrange for an equation to solve t. Computers can't do maths yo.
        z = []
        for i in range(len(planes)):
            if planes[i][0][2] == 0:
                continue
            else:
                #print(planes[i])
                
                xMinusxo = xProbePos-planes[i][1][0]            #first is plane number, second is normal or corner (ranging from 1 to 4), third is x,y,z
                yMinusyo = yProbePos-planes[i][1][1]
                t = -(planes[i][0][0]*xMinusxo + planes[i][0][1]*yMinusyo)/planes[i][0][2] + planes[i][1][2]
                #The formula above is rearranged for t (which is the constraint) for the intersection of plane and the probe. The probe is effectively in a fixed position in z, as it only goes vertically down (beam) and doesn't matter which direction (provided no cut off at z axis edges). We will need to change this if there is cutoff along the edges of the scan, across x,y,z all together. Change especially for z. Go through this with Wolfgang on Tuesday (6/11/18) - Today's date is (4/11/18).
                intersection = np.array([xProbePos,yProbePos,t])
                #print(intersection)
                if self.findValidIntersection(planes[i],intersection):
                    z.append(t)
        if z:
            thickness = max(z) - min(z)
            return thickness
    
    def findValidIntersection(self,plane,intersection):          #give u the singular plane, has the normal vector, 
        o1 = self.orient(intersection,plane[1],plane[3],plane[0])
        o2 = self.orient(intersection,plane[3],plane[4],plane[0])
        o3 = self.orient(intersection,plane[4],plane[2],plane[0])
        o4 = self.orient(intersection,plane[2],plane[1],plane[0])
        #print(o1,o2,o3,o4)
        #print(intersection,plane[1],plane[2],plane[3],plane[4])
        
        if o1 and o2 and o3 and o4:
            #print("its true")
            return True
        elif not o1 and not o2 and not o3 and not o4:
            #print("its true")
            return True
        else:
            #print("its false")
            return False
        
    
    def orient(self,q,p1,p2,n):           #q is intersect, p1 & p2 are two points, n is normal
        first = np.cross((p1-q),(p2-q))
        second = int(np.dot(first,n))
        if second > 0:
            return True
        elif second <= 0:
            return False
        
    def findAxis(self,centre,xAxis,yAxis,zAxis,axisAround,ang):
        xAxis -= centre
        yAxis -= centre
        zAxis -= centre
        if axisAround is 'y':
            rotateQuaternion = Quaternion(axis = yAxis, angle = ang*math.pi/180)
            xAxis = rotateQuaternion.rotate(xAxis) 
            zAxis = rotateQuaternion.rotate(zAxis)
        elif axisAround is 'x':
            rotateQuaternion = Quaternion(axis = xAxis, angle = ang*math.pi/180)
            yAxis = rotateQuaternion.rotate(yAxis)
            zAxis = rotateQuaternion.rotate(zAxis)
        elif axisAround is 'z':
            rotateQuaternion = Quaternion(axis = zAxis, angle = ang*math.pi/180)
            xAxis = rotateQuaternion.rotate(xAxis)
            yAxis = rotateQuaternion.rotate(yAxis)
        
        xAxis += centre
        yAxis += centre
        zAxis += centre
        self.xAxis = xAxis
        self.yAxis = yAxis
        self.zAxis = zAxis
        
        

#def findRegion(self)
    #do something Will be overloaded later on.




#Add future function here to calculate thickness from probe position I guess. Maybe not as we don't want to create new cuboid object
#for each iteration of probe position, that would be dumb.
 
        
#Maybe change this to spherical polars later on? and the cylinder to cylindrical polars? Would that have any benefit? 

class cylinder(objectType):
	def __init__(self,material,alpha,beta,gamma,xPos,yPos,zPos,xProbeRange,yProbeRange,r,l):
		super().__init__(material,alpha,beta,gamma,xPos,yPos,zPos,xProbeRange,yProbeRange)
		self.r = r	
		self.l = l		#r for radius, l for length (across cylinder)

#Possibly cynlindrical polars who knows

#Add extra shapes later. Keep it simple for now. Functions for these?






		

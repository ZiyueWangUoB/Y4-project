#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 15:08:45 2018

@author: ziyuewang
"""

import object
import numpy as np
import math
from pyquaternion import Quaternion



class cuboid(object.objectType):
    def __init__(self,material,deformation,randomQuarternion,xPos,yPos,zPos,xProbeRange,yProbeRange,a,b,c):      #xPos,yPos,zPos all refer to the centre of the object
        super().__init__(material,randomQuarternion,xPos,yPos,zPos,xProbeRange,yProbeRange)
        self.deformation = deformation
        self.a = a		#a b c are length scales of a cuboid, arbitary
        self.b = b
        self.c = c
        self.xAxis = np.array([1,0,0])
        self.yAxis = np.array([0,1,0])
        self.zAxis = np.array([0,0,1])
        self.corners = self.calculateCornerPosition(self.a,self.b,self.c)           #Calls all the functions to work out the intersection (eventual)


    def generatePlanes(self):            #this is specific for the cuboid shape
        p11 = self.findPlane(self.corners[0],self.corners[1],self.corners[2])            #Does direction of n matter? find out later
        p12 = self.findPlane(self.corners[3],self.corners[2],self.corners[1])
        p21 = self.findPlane(self.corners[4],self.corners[5],self.corners[0])            #Goes in line with our diagram, consistent throughout. Normal vector direction doesn't matter.
        p22 = self.findPlane(self.corners[1],self.corners[0],self.corners[5])
        p31 = self.findPlane(self.corners[4],self.corners[0],self.corners[6])            #This consistency will allow us to work with finding whether the intersection
        p32 = self.findPlane(self.corners[2],self.corners[6],self.corners[0])
        p41 = self.findPlane(self.corners[2],self.corners[3],self.corners[6])            #is within the bounded plane or not!
        p42 = self.findPlane(self.corners[7],self.corners[6],self.corners[3])
        p51 = self.findPlane(self.corners[5],self.corners[4],self.corners[7])
        p52 = self.findPlane(self.corners[6],self.corners[7],self.corners[4])
        p61 = self.findPlane(self.corners[1],self.corners[5],self.corners[3])
        p62 = self.findPlane(self.corners[7],self.corners[3],self.corners[5])
        return [p11,p12,p21,p22,p31,p32,p41,p42,p51,p52,p61,p62]
    
    def calculateCornerPosition(self,a,b,c):
        
        c1 = np.array([-a/2,-b/2,-c/2])         #The way this sets it up is for the centre of the object to be around
        c2 = np.array([a/2,-b/2.,-c/2])         #0,0,0 allows the quaternion rotation to be easier.
        c3 = np.array([-a/2,-b/2,c/2])
        c4 = np.array([a/2,-b/2,c/2])
        c5 = np.array([-a/2,b/2,-c/2])
        c6 = np.array([a/2,b/2,-c/2])
        c7 = np.array([-a/2,b/2,c/2])
        c8 = np.array([a/2,b/2,c/2])
        corners = [c1,c2,c3,c4,c5,c6,c7,c8] 
        for i in range(len(corners)):
            corners[i] += np.array([self.xPos,self.yPos,self.zPos])
        return corners     #corners are set in the way sketched in notebook, will include diagram later
        
    #def        #We need to write a function here that resets the object back to the 0,0,0 centre, for rotations, then pushes it back to original location
     
    
    def rotateCorners(self,xPos,yPos,zPos):
        
        
        #Needs to rotate the axis after each rotation, otherwise it won't work! 
        totalRotationQuaternion = self.randomQuarternion       #Should generate a random uniform quaternion across the rotation space
        print(self.randomQuarternion)
        corn = self.corners
        
        for x in range(len(self.corners)):
            self.corners[x] -= [self.xPos, self.yPos, self.zPos]
            self.corners[x] = totalRotationQuaternion.rotate(corn[x])
            self.corners[x] += [self.xPos, self.yPos, self.zPos]
        
    def doRotation(self):
        self.rotateCorners(self.xPos,self.yPos,self.zPos)
        self.planes = self.generatePlanes()          #Up to planes is still working, rotation is intact

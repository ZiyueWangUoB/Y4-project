#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Created on Thu Nov  1 14:40:06 2018
    
    @author: ziyuewang
    """


#Triangular based pyramid

import object
import numpy as np
import math
from pyquaternion import Quaternion

class tripyr(object.objectType):
    def __init__(self,material,deformation,randomQuarternion,xPos,yPos,zPos,xProbeRange,yProbeRange,corner,cornA,cornB,cornC,xAxis,yAxis,zAxis):
        #corner is defined as the corner the deformation is occuring on the cuboid/other shape.
        super().__init__(material,randomQuarternion,xPos,yPos,zPos,xProbeRange,yProbeRange)
        self.corners = np.array([corner,cornA,cornB,cornC])
        self.xAxis = np.array([1,0,0])
        self.yAxis = np.array([0,1,0])
        self.zAxis = np.array([0,0,1])
        self.deformation = deformation
        self.planes = self.generatePlanes(self.corners)
    
    
    def doRotation(self):
        corners = self.rotateCorners(self.corners,self.xPos,self.yPos,self.zPos)
        self.planes = self.generatePlanes(corners)
    
    def rotateCorners(self,corners,xPos,yPos,zPos):
        
        totalRotationQuaternion = self.randomQuarternion
        
        for x in range(len(corners)):
            corners[x] -= [xPos, yPos, zPos]
            corners[x] = totalRotationQuaternion.rotate(corners[x])
            corners[x] += [xPos, yPos, zPos]
            
        return corners
        
    def generatePlanes(self,corners):
        p1 = self.findPlane(corners[1],corners[2],corners[3])
        p2 = self.findPlane(corners[0],corners[2],corners[3])
        p3 = self.findPlane(corners[0],corners[1],corners[3])
        p4 = self.findPlane(corners[0],corners[1],corners[2])
        return [p1,p2,p3,p4]
    
	'''
    def findValidIntersection(self,plane,intersection):          #give u the singular plane, has the normal vector, 
        o1 = self.orient(intersection,plane[2],plane[1],plane[0])
        o2 = self.orient(intersection,plane[3],plane[2],plane[0])
        o3 = self.orient(intersection,plane[1],plane[3],plane[0])
        #print(intersection,plane[2],plane[3],plane[0])
        
        if o1 and o2 and o3:
            #print("its true")
            return True
        elif not o1 and not o2 and not o3:
            #print("its true")
            return True
        else:
            #print("its false")
            return False
	'''
        
        
        

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
    def __init__(self,material,deformation,alpha,beta,gamma,xPos,yPos,zPos,xProbeRange,yProbeRange,corner,cornA,cornB,cornC,xAxis,yAxis,zAxis):
        #corner is defined as the corner the deformation is occuring on the cuboid/other shape.
        super().__init__(material,alpha,beta,gamma,xPos,yPos,zPos,xProbeRange,yProbeRange)
        self.corners = np.array([corner,cornA,cornB,cornC])
        self.xAxis = np.array([1,0,0])
        self.yAxis = np.array([0,1,0])
        self.zAxis = np.array([0,0,1])
        self.deformation = deformation
        self.planes = self.generatePlanes(self.corners)
        
    def findPlane(self,c1,c2,c3): #This is generic for any plane
        vector12 = c2 - c1
        vector13 = c3 - c1
        n = np.cross(vector12,vector13)
        nNorm = n/np.linalg.norm(n)
        return nNorm, c1, c2, c3
    
    def doRotation(self):
        corners = self.rotateCorners(self.corners,self.xPos,self.yPos,self.zPos)
        self.planes = self.generatePlanes(corners)
    
    def rotateCorners(self,corners,xPos,yPos,zPos):
        #Since this class is going to be made for deformations, the corners will be rotated as the cuboid object
        #is rotated, hence they rotate in the same fashion, around the same axis and central point. 
        centre = [xPos,yPos,zPos]
        alphaQuaternion = Quaternion(axis= self.yAxis, angle = self.alpha*math.pi/180)
        self.findAxis(centre,self.xAxis,self.yAxis,self.zAxis,'y',self.alpha)
        betaQuaternion = Quaternion(axis=self.xAxis, angle = self.beta*math.pi/180)
        self.findAxis(centre,self.xAxis,self.yAxis,self.zAxis,'x',self.beta)
        gammaQuaternion = Quaternion(axis=self.zAxis, angle = self.gamma*math.pi/180)
        self.findAxis(centre,self.xAxis,self.yAxis,self.zAxis,'z',self.gamma)
        
        totalRotationQuaternion = alphaQuaternion*betaQuaternion*gammaQuaternion
        
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

        
        
        

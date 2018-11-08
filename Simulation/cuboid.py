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
    def __init__(self,material,alpha,beta,gamma,xPos,yPos,zPos,xProbeRange,yProbeRange,a,b,c):      #xPos,yPos,zPos all refer to the centre of the object
        super().__init__(material,alpha,beta,gamma,xPos,yPos,zPos,xProbeRange,yProbeRange)
        self.a = a		#a b c are length scales of a cuboid, arbitary
        self.b = b
        self.c = c
        self.xAxis = np.array([1,0,0])
        self.yAxis = np.array([0,1,0])
        self.zAxis = np.array([0,0,1])
        self.thicknessMatrix = self.calcThicknessMatrix()
        #print(self.thicknessMatrix)
        #Place these calls into calcThickness later on to make it straightforward and less messy

        #print(self.Planes)


    def generatePlanes(self):            #this is specific for the cuboid shape
        p1 = self.findPlane(self.corners[0],self.corners[1],self.corners[2],self.corners[3])            #Does direction of n matter? find out later
        p2 = self.findPlane(self.corners[4],self.corners[5],self.corners[0],self.corners[1])            #Goes in line with our diagram, consistent throughout. Normal vector direction doesn't matter. 
        p3 = self.findPlane(self.corners[4],self.corners[0],self.corners[6],self.corners[2])            #This consistency will allow us to work with finding whether the intersection
        p4 = self.findPlane(self.corners[2],self.corners[3],self.corners[6],self.corners[7])            #is within the bounded plane or not!
        p5 = self.findPlane(self.corners[5],self.corners[4],self.corners[7],self.corners[6])
        p6 = self.findPlane(self.corners[1],self.corners[5],self.corners[3],self.corners[7])
        return [p1,p2,p3,p4,p5,p6]
    
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
        
        #Rotating corners also rotates the axis!
        centre = [xPos,yPos,zPos]
        alphaQuaternion = Quaternion(axis= self.yAxis, angle = self.alpha*math.pi/180)               #bare in mind rotations in y is inverted to what we think - refer to notebook. X and z axis rotation is same as in diagrams
        self.findAxis(centre,self.xAxis,self.yAxis,self.zAxis,'y',self.alpha)
        betaQuaternion = Quaternion(axis=self.xAxis, angle = self.beta*math.pi/180)
        self.findAxis(centre,self.xAxis,self.yAxis,self.zAxis,'x',self.beta)
        gammaQuaternion = Quaternion(axis=[0,0,1], angle = self.gamma*math.pi/180)
        self.findAxis(centre,self.xAxis,self.yAxis,self.zAxis,'z',self.gamma)
        
        #Needs to rotate the axis after each rotation, otherwise it won't work! 
        totalRotationQuaternion = alphaQuaternion*betaQuaternion*gammaQuaternion
        
        corn = self.corners         #Remove later if it's fine
        
        for x in range(len(self.corners)):
            self.corners[x] -= [self.xPos, self.yPos, self.zPos]
            self.corners[x] = totalRotationQuaternion.rotate(corn[x])
            self.corners[x] += [self.xPos, self.yPos, self.zPos]
        
    def calcThicknessMatrix(self):

        self.corners = self.calculateCornerPosition(self.a,self.b,self.c)           #Calls all the functions to work out the intersection (eventual)
        self.rotateCorners(self.xPos,self.yPos,self.zPos)
        self.Planes = self.generatePlanes()          #Up to planes is still working, rotation is intact
        thicknessMatrix = np.zeros((len(self.xProbeRange),len(self.yProbeRange)))
        for i in range(len(self.xProbeRange)):
            for u in range (len(self.yProbeRange)):
               intersects = self.findIntersectionThickness(self.Planes,i,u)
               if intersects:
                    thicknessMatrix[i][u] = intersects                              #Outputs the intersects on thickness matrix!
        intersects = self.findIntersectionThickness(self.Planes,i,u)            
       # print(thicknessMatrix[50][50])
            
        return thicknessMatrix
    




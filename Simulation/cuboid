#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 01:06:02 2018

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
        self.calcThicknessMatrix()
        
        #Place these calls into calcThickness later on to make it straightforward and less messy

        #print(self.Planes)


    def generatePlanes(self):            #this is specific for the cuboid shape
        p1 = self.findPlane(self.corners[0],self.corners[1],self.corners[2])            #Does direction of n matter? find out later
        p2 = self.findPlane(self.corners[0],self.corners[4],self.corners[1])            #These all point out from the centre.
        p3 = self.findPlane(self.corners[0],self.corners[2],self.corners[4])
        p4 = self.findPlane(self.corners[2],self.corners[6],self.corners[3])
        p5 = self.findPlane(self.corners[4],self.corners[6],self.corners[5])
        p6 = self.findPlane(self.corners[1],self.corners[5],self.corners[3])
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
        return [c1,c2,c3,c4,c5,c6,c7,c8]           #corners are set in the way sketched in notebook, will include diagram later
        
    #def        #We need to write a function here that resets the object back to the 0,0,0 centre, for rotations, then pushes it back to original location
     
    
    def rotateCorners(self):
        
        alphaQuaternion = Quaternion(axis=[0,-1,0], angle = self.alpha*math.pi/180)               #bare in mind rotations in y is inverted to what we think - refer to notebook. X and z axis rotation is same as in diagrams
        betaQuaternion = Quaternion(axis=[1,0,0,], angle = self.beta*math.pi/180)
        gammaQuaternion = Quaternion(axis=[0,0,1], angle = self.gamma*math.pi/180)
        totalRotationQuaternion = alphaQuaternion*betaQuaternion*gammaQuaternion
        
        corn = self.corners         #Remove later if it's fine
        
        for x in range(len(self.corners)):
            self.corners[x] = totalRotationQuaternion.rotate(corn[x])
            self.corners[x] += [self.xPos, self.yPos, self.zPos]
        
    def calcThicknessMatrix(self):
        self.corners = self.calculateCornerPosition(self.a,self.b,self.c)
        self.rotateCorners()
        self.Planes = self.generatePlanes()
        self.thicknessMatrix = np.zeros((len(self.xProbeRange),len(self.yProbeRange)))
        for i in range(len(self.xProbeRange)):
            for u in range (len(self.yProbeRange)):
                self.findIntersection(self.Planes,i,u)
        return self.thicknessMatrix


#Add future function here to calculate thickness from probe position I guess. Maybe not as we don't want to create new cuboid object
#for each iteration of probe position, that would be dumb.

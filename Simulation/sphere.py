#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 15:15:37 2018

@author: ziyuewang
"""
import object
import numpy as np
import math

class sphere(object.objectType):
    def __init__(self,material,alpha,beta,gamma,xPos,yPos,zPos,xProbeRange,yProbeRange,r):
        super().__init__(material,alpha,beta,gamma,xPos,yPos,zPos,xProbeRange,yProbeRange)		#Consider removing the angles since sphere doesn't tilt - may be a waste of memory
        self.r = r		#radius
        self.thicknessMatrix = self.calcThicknessMatrix()
        
        #Not including z position as it is trivial in STEM. The thickness is still the same regardless of z position.
    def calcThickness(self,xProbePos,yProbePos):
        zSqr = self.r**2- (xProbePos-self.xPos)**2 - (yProbePos-self.yPos)**2
       #print(str(self.r) + " " + str(xProbePos) + " " + str(self.xPos) + " " + str(yProbePos) + " " + str(self.yPos))
       #print(zSqr)
        if zSqr > 0:                            #Really lazy check. What essentially happened is we've placed the sphere in a box, and the function below checks 
            z = float(math.sqrt(zSqr))          #if the probe is within the region of the box. Then it tries to probe it. But at the corners of the box, the sphere
            return abs(z*2)                     #doesn't touch it. Hence we got negative numbers. This check is a lazy check, correct later, checks for negatives
        else:                                   #and just returns as 0. Probably a better and more effective way than this, but for now keep it at it is.
            return 0
        
        
        
        
    def calcThicknessMatrix(self):
        thicknessMatrix = np.zeros((len(self.xProbeRange),len(self.yProbeRange)))
        for i in range(len(self.xProbeRange)):              #For the range of the probe
            for u in range (len(self.yProbeRange)):
                if i in range(self.xPos-self.r,self.xPos+self.r+1) and u in range(self.yPos-self.r,self.yPos+self.r+1):         #this confirms that it's in the range
                    thicknessMatrix[i][u] = self.calcThickness(i,u)
                    return thicknessMatrix
        
       
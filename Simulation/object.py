#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 14:40:06 2018

@author: ziyuewang
"""
#This file is made for the objects, starting with base class and children
import numpy as np
import math


class objectType:
	#Alpha Beta Gamma are the tilts or angles to the x,y,z planes respectively.
    def __init__(self,material,alpha,beta,gamma,xPos,yPos,xProbeRange,yProbeRange):
        self.material = material
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.xPos = xPos
        self.yPos = yPos
        self.xProbeRange = xProbeRange
        self.yProbeRange = yProbeRange
#Add future function here to calculate tilt, just stating variables for now

class cuboid(objectType):
    def __init__(self,material,alpha,beta,gamma,xPos,yPos,xProbeRange,yProbeRange,a,b,c):
        super().__init__(material,alpha,beta,gamma,xPos,yPos,xProbeRange,yProbeRange)
        self.a = a		#a b c are length scales of a cuboid, arbitary
        self.b = b
        self.c = c
        
    def calcThickness(self):
        self.thicknessMatrix = np.zeros((len(self.xProbeRange),len(self.yProbeRange)))
        for i in range(len(self.xProbeRange)):
            for u in range (len(self.yProbeRange)):
                self.thicknessMatrix[i][u] = self.b
        return self.thicknessMatrix


#Add future function here to calculate thickness from probe position I guess. Maybe not as we don't want to create new cuboid object
#for each iteration of probe position, that would be dumb.


class sphere(objectType):
    def __init__(self,material,alpha,beta,gamma,xPos,yPos,xProbeRange,yProbeRange,r):
        super().__init__(material,alpha,beta,gamma,xPos,yPos,xProbeRange,yProbeRange)		#Consider removing the angles since sphere doesn't tilt - may be a waste of memory
        self.r = r		#radius
        
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
        self.thicknessMatrix = np.zeros((len(self.xProbeRange),len(self.yProbeRange)))
        for i in range(len(self.xProbeRange)):              #For the range of the probe
            for u in range (len(self.yProbeRange)):
                if i in range(self.xPos-self.r,self.xPos+self.r+1) and u in range(self.yPos-self.r,self.yPos+self.r+1):         #this confirms that it's in the range
                    self.thicknessMatrix[i][u] = self.calcThickness(i,u)
                    
        
        
        
#Maybe change this to spherical polars later on? and the cylinder to cylindrical polars? Would that have any benefit? 

class cylinder(objectType):
	def __init__(self,material,alpha,beta,gamma,xPos,yPos,xProbeRange,yProbeRange,r,l):
		super().__init__(material,alpha,beta,gamma,xPos,yPos,xProbeRange,yProbeRange)
		self.r = r	
		self.l = l		#r for radius, l for length (across cylinder)

#Possibly cynlindrical polars who knows

#Add extra shapes later. Keep it simple for now. Functions for these?






		

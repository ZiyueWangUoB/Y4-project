#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  1 14:40:06 2018

@author: ziyuewang
"""
#This file is made for the objects, starting with base class and children
import numpy as np


class objectType:
	#Alpha Beta Gamma are the tilts or angles to the x,y,z planes respectively.
    def __init__(self,material,alpha,beta,gamma,xStart,yStart,xProbeRange,yProbeRange):
        self.material = material
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.xStart = xStart
        self.yStart = yStart
        self.xProbeRange = xProbeRange
        self.yProbeRange = yProbeRange
#Add future function here to calculate tilt, just stating variables for now

class cuboid(objectType):
    def __init__(self,material,alpha,beta,gamma,xStart,yStart,xProbeRange,yProbeRange,a,b,c):
        super().__init__(material,alpha,beta,gamma,xProbeRange,yProbeRange)
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
	def __init(self,material,alpha,beta,gamma,xStart,yStart,xProbeRange,yProbeRange,r):
		super().__init__(material,alpha,beta,gamma,xProbeRange,yProbeRange)		#Consider removing the angles since sphere doesn't tilt - may be a waste of memory
		self.r = r		#radius	
#Maybe change this to spherical polars later on? and the cylinder to cylindrical polars? Would that have any benefit? 

class cylinder(objectType):
	def __init__(self,material,alpha,beta,gamma,xStart,yStart,xProbeRange,yProbeRange,r,l):
		super().__init__(material,alpha,beta,gamma,xProbeRange,yProbeRange)
		self.r = r	
		self.l = l		#r for radius, l for length (across cylinder)

#Possibly cynlindrical polars who knows

#Add extra shapes later. Keep it simple for now. Functions for these?






		

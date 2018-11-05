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
        intersections = []
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
                #    print('Valid')
                    intersections.append(intersection)
                #print(intersections)
        if intersections:
            thickness = intersections[-1][2] - intersections[0][2]
            return thickness
    
    def findValidIntersection(self,plane,intersection):          #give u the singular plane, has the normal vector, 
        o1 = self.orient(intersection,plane[1],plane[3],plane[0])
        o2 = self.orient(intersection,plane[3],plane[4],plane[0])
        o3 = self.orient(intersection,plane[4],plane[2],plane[0])
        o4 = self.orient(intersection,plane[2],plane[1],plane[0])
        
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
        second = np.dot(first,n)
        if second > 0:
            return True
        elif second < 0:
            return False

#def findRegion(self)
    #do something Will be overloaded later on.


class cuboid(objectType):
    def __init__(self,material,alpha,beta,gamma,xPos,yPos,zPos,xProbeRange,yProbeRange,a,b,c):      #xPos,yPos,zPos all refer to the centre of the object
        super().__init__(material,alpha,beta,gamma,xPos,yPos,zPos,xProbeRange,yProbeRange)
        self.a = a		#a b c are length scales of a cuboid, arbitary
        self.b = b
        self.c = c
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
        self.corners = self.calculateCornerPosition(self.a,self.b,self.c)           #Calls all the functions to work out the intersection (eventual)
        self.rotateCorners()
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
    


#Add future function here to calculate thickness from probe position I guess. Maybe not as we don't want to create new cuboid object
#for each iteration of probe position, that would be dumb.


class sphere(objectType):
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
        
        
        
#Maybe change this to spherical polars later on? and the cylinder to cylindrical polars? Would that have any benefit? 

class cylinder(objectType):
	def __init__(self,material,alpha,beta,gamma,xPos,yPos,zPos,xProbeRange,yProbeRange,r,l):
		super().__init__(material,alpha,beta,gamma,xPos,yPos,zPos,xProbeRange,yProbeRange)
		self.r = r	
		self.l = l		#r for radius, l for length (across cylinder)

#Possibly cynlindrical polars who knows

#Add extra shapes later. Keep it simple for now. Functions for these?






		

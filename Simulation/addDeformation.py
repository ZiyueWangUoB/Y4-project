#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 18:51:24 2018

@author: ziyuewang
add deformation class
"""

import numpy as np
import random

class addDeformation:
    def __init__(self,theObject,objectType,cornersToDeform,sf):
        self.object = theObject
        self.corners = theObject.corners
        #Add deformation in the rest of the constructor
        self.deformArray = self.classObject(objectType,cornersToDeform,sf)
        self.sf = sf

    def classObject(self,objectType,cornersToDeform,sf):
        deformArray = []
        if objectType is 'cuboid':
            vcorn = self.findAxisCuboid(self.corners)
            #numOfDeformations = np.random.randint(0,8)
            #numOfDeformations = 8
            #random.sample(range(0,8),numOfDeformations)
            deformTheseCorners = cornersToDeform
            
            #Need to think of a way so that the deformed corners don't go as 1,2,3,4,5,6 e.t.c
            #For now we set the specific number
            
            for i in range(len(deformTheseCorners)):
                u = self.cornerDeformation(vcorn[deformTheseCorners[i]],deformTheseCorners[i],sf)
                deformArray.append(u)
                
        return deformArray
        
    def cornerDeformation(self,vcorn,cornerNum,sf):
        
        c1 = self.corners[cornerNum]
        a = np.random.randint(20*sf,30*sf)              #Make these randomly generate later
        b = np.random.randint(20*sf,30*sf)
        c = np.random.randint(20*sf,30*sf)
        
        #a = 50*sf
        #b = 50*sf
        #c = 50*sf
        
        
        c2 = c1 + a*vcorn[0]
        c3 = c1 + b*vcorn[1]
        c4 = c1 + c*vcorn[2]
        return c1,c2,c3,c4
    
    
    
    
    
    
    
    
    def findAxisCuboid(self,corners):
        v = [[[] for x in range(8)] for y in range(8)]
        vcorn = [[[] for x in range(3)] for y in range(8)]
        
        
        v12 = corners[1] - corners[0]
        v[0][1] = v12/np.linalg.norm(v12)
        v13 = corners[2] - corners[0]
        v[0][2] = v13/np.linalg.norm(v13)
        v15 = corners[4] - corners[0]
        v[0][4] = v15/np.linalg.norm(v15)
        vcorn[0][0] = v[0][1]
        vcorn[0][1] = v[0][2]
        vcorn[0][2] = v[0][4]
        
        v24 = corners[3] - corners[1]
        v[1][3] = v24/np.linalg.norm(v24)
        v26 = corners[5] - corners[1]
        v[1][5] = v26/np.linalg.norm(v26)
        v[1][0] = -v[0][1]
        vcorn[1][0] = v[1][3]
        vcorn[1][1] = v[1][5]
        vcorn[1][2] = v[1][0]
        
        
        v34 = corners[3] - corners[2]
        v[2][3] = v34/np.linalg.norm(v34)
        v37 = corners[6] - corners[2]
        v[2][6] = v37/np.linalg.norm(v37)
        v[2][0] = -v[0][2]
        vcorn[2][0] = v[2][3]
        vcorn[2][1] = v[2][6]
        vcorn[2][2] = v[2][0]
        
        
        v48 = corners[7] - corners[3]
        v[3][7] = v48/np.linalg.norm(v48)
        v[3][1] = -v[1][3]
        v[3][2] = -v[2][3]
        vcorn[3][0] = v[3][7]
        vcorn[3][1] = v[3][1]
        vcorn[3][2] = v[3][2]
        
        v56 = corners[5] - corners[4]
        v[4][5] = v56/np.linalg.norm(v56)
        v57 = corners[6] - corners[4]
        v[4][6] = v57/np.linalg.norm(v57)
        v[4][0] = -v[0][4]
        vcorn[4][0] = v[4][5]
        vcorn[4][1] = v[4][6]
        vcorn[4][2] = v[4][0]
        
        
        v68 = corners[7] - corners[5]
        v[5][7] = v68/np.linalg.norm(v68)
        v[5][1] = -v[1][5]
        v[5][4] = -v[4][5]
        vcorn[5][0] = v[5][7]
        vcorn[5][1] = v[5][1]
        vcorn[5][2] = v[5][4]
        
        v78 = corners[7] - corners[6]
        v[6][7] = v78/np.linalg.norm(v78)
        v[6][4] = -v[4][6]
        v[6][2] = -v[2][6]
        vcorn[6][0] = v[6][7]
        vcorn[6][1] = v[6][4]
        vcorn[6][2] = v[6][2]

        v[7][6] = -v[6][7]
        v[7][5] = -v[5][7]
        v[7][3] = -v[3][7]
        vcorn[7][0] = v[7][6]
        vcorn[7][1] = v[7][5]
        vcorn[7][2] = v[7][3]

        return vcorn
         






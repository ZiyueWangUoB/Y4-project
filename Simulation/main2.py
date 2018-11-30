#31/10/2018 
#This is the main file where most stuff is done. Classes will be written as their own modules yeah. 
import matplotlib.pyplot as plt
import scipy.ndimage.filters
import math
import numpy as np
from multiprocessing import Pool

import tripyr
import cuboid
import sphere
import addDeformation as aD
import sys
import time

objects = []                #Leaving it here as a global variable, so that the functions can read it.
xRange = [i for i in range(0,100)]        #100x100 scan for probe, across 100x100
yRange = [i for i in range(0,100)]
zRange = [i for i in range(0,100)]


#Set of functions
#Function to add noise to the matrix
def addPoissonNoise(Matrix):
    for i in range(len(xRange)):
        for u in range (len(yRange)):
            noise = np.random.poisson(8)            #How big should the noise be? Any ideas? #relative to mean intensity
            Matrix[i][u] += noise
            
def calcThicknessMatrix(objects,xProbeRange,yProbeRange):
    p = Pool()
    p.map(y,xRange)
    thicknessMatrix = np.zeros((len(xProbeRange),len(yProbeRange)))
    for n in xRange:
        #thicknessMatrix.append(y(n))
        thicknessMatrix[n][:] += y(n)
    print(thicknessMatrix[0])
    return thicknessMatrix

def y(i):               #Function for multiprocessing to call
    thicknessList = np.zeros(len(yRange))
    for u in range (len(yRange)):
        #Random probability for the object to rotate during imaging, by a small angle.
            #rotRand = np.random.randint(0,2)
            
        rotRand = 0
        if rotRand == 1:
            alphaRand = np.random.randint(0,3)
            betaRand = np.random.randint(0,3)
            gammaRand = np.random.randint(0,3)
        
        for a in range(len(objects)):
            thisObject = objects[a]
            
            if rotRand == 1:
                thisObject.alpha = alphaRand
                thisObject.beta = betaRand
                thisObject.gamma = gammaRand
            
            intersects = thisObject.findIntersectionThickness(thisObject.planes,i,u)
            if intersects:
                if not thisObject.deformation:
                    thicknessList[u] += intersects                              #Thickness Lists
                else:
                    thicknessList[u] -= intersects
    return thicknessList


def rotateThroughBy90(objects):
    for a in range(len(objects)):
        thisObject = objects[a]
        thisObject.alpha = 1
        thisObject.beta = 1
        thisObject.gamma = 1
        thisObject.doRotation()
    return objects



for g in range(1):

    #Generating an test object, let a cube.

    #Generate random parameters of the cube
    aRand = np.random.randint(40,50)
    bRand = np.random.randint(40,50)
    cRand = np.random.randint(40,50)

    #Generate random numbers for start position
    xPosRandom = np.random.randint(45,56)         #This is to make sure the object stays within the confides of the image!
    yPosRandom = np.random.randint(45,56)          #Centered at between 45 and 55.


    #rRand = np.random.randint(cLMax/10,cLMax/5)
    #sphere = sphere.sphere("xs",False,0,0,0,xPosRandom,yPosRandom,cLMax,xRange,yRange,rRand)

    #sphere.calcThicknessMatrix()

    alphaRand = np.random.randint(0,360)
    betaRand = np.random.randint(0,360)
    gammaRand = np.random.randint(0,360)


    cube = cuboid.cuboid("cmj",False,alphaRand,betaRand,gammaRand,xPosRandom,yPosRandom,50,xRange,yRange,aRand,bRand,cRand)
    #cube = cuboid.cuboid('cmj',False,20,31,21,50,50,50,xRange,yRange,12,30,50)
    objects.append(cube)

    #deformations calculated and set here
    deforms = aD.addDeformation(cube,'cuboid')
    dA = deforms.deformArray

    #The deformations are tripyr which are created in this loop
    for i in range(len(dA)):
        deformation = tripyr.tripyr("xcl",True,alphaRand,betaRand,gammaRand,xPosRandom,yPosRandom,50,xRange,yRange,dA[i][0],dA[i][1],dA[i][2],dA[i][3],cube.xAxis,cube.yAxis,cube.zAxis)
        objects.append(deformation)


    for i in range(len(objects)):
        objects[i].doRotation()
    

    #file = open('cube orientations.txt', 'w')
    #file.write(str(dA[:][0]))
    #file.close()

    start_time = time.time()
    image = calcThicknessMatrix(objects,xRange,yRange) + 10
    elapsed_time = time.time() - start_time
    print(elapsed_time)

    #Adding gaussian blur
    image = scipy.ndimage.filters.gaussian_filter(image,1)
    
    #Adding poisson noise
    addPoissonNoise(image)
    #plt.figure(figsize=(5,5))
    plt.pcolormesh(xRange, yRange, image, cmap="Greys_r")
    
    plt.show()
    #plt.savefig('SimulationImages/Spheres/plot'+str(sys.argv[i])+'.png')     #sys.argv is the input from the bash script
    #plt.savefig('/home/z/Documents/pics/1deform/image' + str(sys.argv[1]) + '.png', bbox_inches='tight', pad_inches = 0)     #sys.argv is the input from the bash script made for 1deform on linux rn
    #plt.imsave('/home/z/Documents/pics/0deform/image' + str(sys.argv[1]) + '.jpg',image,format='jpg',cmap = 'gray')
    #plt.imsave('/home/z/Documents/pics/0deform/test1.jpg',image,format='jpg',cmap='gray')
    #plt.close()



#31/10/2018 
#This is the main file where most stuff is done. Classes will be written as their own modules yeah. 
import matplotlib.pyplot as plt
import scipy.ndimage.filters
import math
import numpy as np

import tripyr
import cuboid
import sphere
import addDeformation as aD
import sys

#Set of functions
#Function to add noise to the matrix
def addPoissonNoise(Matrix):
    for i in range(len(xRange)):
        for u in range (len(yRange)):
            noise = np.random.poisson(5)            #How big should the noise be? Any ideas? #relative to mean intensity
            Matrix[i][u] += noise
            
def calcThicknessMatrix(objects,xProbeRange,yProbeRange):
    thicknessMatrix = np.zeros((len(xProbeRange),len(yProbeRange)))
    for i in range(len(xProbeRange)):
        for u in range (len(yProbeRange)):
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
                        thicknessMatrix[i][u] += intersects                              #Outputs the intersects on thickness matrix!
                    else:
                        thicknessMatrix[i][u] -= intersects
        # print(thicknessMatrix[50][50])

    return thicknessMatrix

def rotateThroughBy90(objects):
    for a in range(len(objects)):
        thisObject = objects[a]
        thisObject.alpha = 1
        thisObject.beta = 1
        thisObject.gamma = 1
        thisObject.doRotation()
    return objects

xRange = [i for i in range(0,100)]        #100x100 scan for probe, across 100x100
yRange = [i for i in range(0,100)]
zRange = [i for i in range(0,100)]


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
    objects = [cube]

    #deformations calculated and set here
    deformTheseCorners = sys.argv[2].split(',')
    deformTheseCornersResult = list(map(int,deformTheseCorners))        #Only problem is we can't not deform any corners, which is fine cuz that set has already been done. We can adjust for later tho!
    deforms = aD.addDeformation(cube,'cuboid',deformTheseCornersResult)
    dA = deforms.deformArray

    #The deformations are tripyr which are created in this loop
    for i in range(len(dA)):
        deformation = tripyr.tripyr("xcl",True,alphaRand,betaRand,gammaRand,xPosRandom,yPosRandom,50,xRange,yRange,dA[i][0],dA[i][1],dA[i][2],dA[i][3],cube.xAxis,cube.yAxis,cube.zAxis)
        objects.append(deformation)


    for i in range(len(objects)):
        objects[i].doRotation()
    

    file = open('cube orientations.txt', 'w')
    file.write(str(dA[:][0]))
    file.close()


    image = calcThicknessMatrix(objects,xRange,yRange) + 10

    #Adding gaussian blur
    image = scipy.ndimage.filters.gaussian_filter(image,1)
    
    #Adding poisson noise
    addPoissonNoise(image)
    #plt.figure(figsize=(5,5))
    plt.pcolormesh(xRange, yRange, image, cmap="Greys_r")
    
    #plt.show()
    #plt.savefig('SimulationImages/Spheres/plot'+str(sys.argv[i])+'.png')     #sys.argv is the input from the bash script
    #plt.savefig('/home/z/Documents/pics/1deform/image' + str(sys.argv[1]) + '.png', bbox_inches='tight', pad_inches = 0)     #sys.argv is the input from the bash script made for 1deform on linux rn
    plt.imsave('/home/z/Documents/pics/' + str(sys.argv[3]) + '/image' + str(sys.argv[1]) + '.png',image,format='png',cmap = 'gray')
    plt.close()



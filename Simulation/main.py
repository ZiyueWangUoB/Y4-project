#31/10/2018 :w

#This is the main file where most stuff is done. Classes will be written as their own modules yeah.
#Nothing really to update, just putting something in to push lol
import matplotlib.pyplot as plt
import scipy.ndimage.filters
import math
import numpy as np
import time
import tripyr
import cuboid
import sphere
import addDeformation as aD
import sys
import random

sf = 1

#Let N be the number of events at each pixel, where the total is a constant. Or just keep N a factor? So as we jump from 128 to 256, sf = 2 from 1, then N per pixel will drop by 4. 
#To start off then, let's set N to 8 (so max we can go is 1024 -> 512 - > 256 -> 128)
N = 16/sf/sf
#Scales with sf (scale factor). Will reach min at when 1 at 1024 (as this scales with 1/sf^2)

#Set of functions
#Function to add noise to the matrix
def addPoissonNoise(Matrix):
    #Poisson noise is singal dependent!
    noise_mask = np.random.poisson(Matrix)
    return noise_mask+Matrix

def findMaxAndMin(mainObject):
    corners = mainObject.corners
    zipped = zip(*corners)          #Converts rows to columns basically
    newArray = np.array([i for i in zipped])         #Makes it to a readable thing - now we can find max and min of x,y,z
    minX = np.amin(newArray[0])
    maxX = np.amax(newArray[0])
    minY = np.amin(newArray[1])
    maxY = np.amax(newArray[1])
    return [(minX,maxX), (minY,maxY)]

'''
def calcThicknessMatrix(objects,xProbeRange,yProbeRange):
    thicknessMatrix = np.zeros((len(xProbeRange),len(yProbeRange)))
    minMax = [findMaxAndMin(objects[i]) for i in range(0,len(objects))]      #Calculate the original min and max values for x and y
    for i in range(len(xProbeRange)):
        if i < minMax[0][0][0] or i > minMax[0][0][1]:
            continue
        for u in range (len(yProbeRange)):
            if u < minMax[0][1][0] or u > minMax[0][1][1]:
                continue
            #Random probability for the object to rotate during imaging, by a small angle.
            rotRand = np.random.randint(0,500)

            
            if rotRand == 1: 
                alphaRand = np.random.randint(-3,3)*0.5
                betaRand = np.random.randint(-3,3)*0.5
                gammaRand = np.random.randint(-3,3)*0.5
                #Also needs to calculate new min and max values for the next loops. 
                minMax = [findMaxAndMin(objects[i]) for i in range(0,len(objects))]
                #print(minMax)


            for a in range(len(objects)):
               # if a == 0:
                #    continue
                thisObject = objects[a]
                
                
                if i < minMax[a][0][0] or i > minMax[a][0][1] or u < minMax[a][1][0] or u > minMax[a][1][1]:
                    continue
                
                intersects = thisObject.findIntersectionThickness(thisObject.planes,i,u)
                if intersects:
                    if not thisObject.deformation:
                        thicknessMatrix[i][u] += intersects                              #Outputs the intersects on thickness matrix!
                    else:
                        thicknessMatrix[i][u] -= intersects
        # print(thicknessMatrix[50][50])

    return thicknessMatrix
'''

def calcThicknessMatrix(objects)



'''
def rotateThroughBy90(objects):
    for a in range(len(objects)):
        thisObject = objects[a]
        thisObject.alpha = 1
        thisObject.beta = 1
        thisObject.gamma = 1
        thisObject.doRotation()
    return objects
    
'''

xRange = [i for i in range(0,int(128*sf))]        #100x100 scan for probe, across 100x100
yRange = [i for i in range(0,int(128*sf))]
zRange = [i for i in range(0,int(128*sf))]



for g in range(1):

    #Generating an test object, let a cube.

    #Generate random parameters of the cube
    aRand = np.random.randint(60*sf,70*sf)
    bRand = np.random.randint(60*sf,70*sf)
    cRand = np.random.randint(60*sf,70*sf)

    #Generate random numbers for start position
    xPosRandom = np.random.randint(59*sf,70*sf)         #This is to make sure the object stays within the confides of the image!
    yPosRandom = np.random.randint(59*sf,70*sf)          #Centered at between 45 and 55.


    #rRand = np.random.randint(cLMax/10,cLMax/5)
    #sphere = sphere.sphere("xs",False,0,0,0,xPosRandom,yPosRandom,cLMax,xRange,yRange,rRand)

    #sphere.calcThicknessMatrix()

    alphaRand = np.random.randint(0,360)
    betaRand = np.random.randint(0,360)
    gammaRand = np.random.randint(0,360)


    cube = cuboid.cuboid("cmj",False,alphaRand,betaRand,gammaRand,xPosRandom,yPosRandom,64*sf,xRange,yRange,aRand,bRand,cRand)
    #cube = cuboid.cuboid("cmj",False,0,0,0,50,50,50,xRange,yRange,30,35,40)
    objects = [cube]
    
    
    '''
    if len(sys.argv) > 1:
    #deformations calculated and set here
        deformTheseCorners = sys.argv[2].split(',')
        deformTheseCornersResult = list(map(int,deformTheseCorners))        #Only problem is we can't not deform any corners, which is fine cuz that set has already been done. We can adjust for later tho!
    else:
        deformTheseCornersResult = []
    '''
    #Alternate method for randomly generating three corners
    if len(sys.argv) > 1:
        deformTheseCornersResult = random.sample(range(0,8),int(sys.argv[2]))
        #print(deformTheseCornersResult)
    else:
        deformTheseCornersResult = []
    print(deformTheseCornersResult)



    deforms = aD.addDeformation(cube,'cuboid',deformTheseCornersResult,sf)
    dA = deforms.deformArray

    #The deformations are tripyr which are created in this loop
    for i in range(len(dA)):
        deformation = tripyr.tripyr("xcl",True,alphaRand,betaRand,gammaRand,xPosRandom,yPosRandom,64*sf,xRange,yRange,dA[i][0],dA[i][1],dA[i][2],dA[i][3],cube.xAxis,cube.yAxis,cube.zAxis)
        objects.append(deformation)

    tSubZero = time.time()
    for i in range(len(objects)):
        objects[i].doRotation()
    #print(time.time()-tSubZero)
    
   # print(objects)

   # file = open('cube orientations.txt', 'w')
   # file.write(str(dA[:][0]))
   # file.close()


	#Need to use function to find the optimal area for the probe to operate. Does this interfere with the rotations while moving? If so how to fix. 
	#We can call the function once here as a preliminary, and call again during the loop?

    t0 = time.time()

    flatBackground = 30*sf              #Flat background from the carbon layer. For now background will scale with scale factor
    image = (calcThicknessMatrix(objects,xRange,yRange) + flatBackground)*N               #Flat background and image will all scale with N, the number of electrons (dose) hitting the atom column 
    print(time.time()-t0)
    #Adding gaussian blur
    image = scipy.ndimage.filters.gaussian_filter(image,sigma=1)
    
    #Adding poisson noise
    image = addPoissonNoise(image)
    #plt.figure(figsize=(5,5))
    
    print(image[0][0])
    print(np.amax(image))
    
    plt.pcolormesh(xRange, yRange, image, cmap="Greys_r")
    
    plt.show()
    #plt.savefig('SimulationImages/Spheres/plot'+str(sys.argv[i])+'.png')     #sys.argv is the input from the bash script
    #plt.savefig('/home/z/Documents/pics/1deform/image' + str(sys.argv[1]) + '.png', bbox_inches='tight', pad_inches = 0)     #sys.argv is the input from the bash script made for 1deform on linux rn
    #plt.imsave('/home/z/Documents/projectImages128/' + str(sys.argv[3]) + '/test' + str(sys.argv[1]) + '.jpg',image,format='jpg',cmap = 'gray')
    #plt.savefig('~/Users/ziyuewang/Documents/Y4\ project/Presentations/rotate' + str(sys.argv[3]) + '.jpg')
    plt.close()



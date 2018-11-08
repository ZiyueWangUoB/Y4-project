#31/10/2018 
#This is the main file where most stuff is done. Classes will be written as their own modules yeah. 
import matplotlib.pyplot as plt
import numpy as np

import cuboid
import sphere
#import sys


#Function to add noise to the matrix
def addPoissonNoise(Matrix):
    for i in range(len(xRange)):
        for u in range (len(yRange)):
            noise = np.random.poisson(rRand)            #How big should the noise be? Any ideas?
            Matrix[i][u] += noise
            
            
            
            

#Probe params
#xRange = [i for i in range(0,int(sys.argv[2]))]        #100x100 scan for probe, across 100x100
#yRange = [i for i in range(0,int(sys.argv[2]))]
#zRange = [i for i in range(0,int(sys.argv[2]))]

xRange = [i for i in range(0,100)]        #100x100 scan for probe, across 100x100
yRange = [i for i in range(0,100)]
zRange = [i for i in range(0,100)]


#Generating an test object, let a cube.

cLMax = 50     #Cube length max

#Generate random parameters of the cube
aRand = np.random.randint(cLMax/10,cLMax)
bRand = np.random.randint(cLMax/10,cLMax)
cRand = np.random.randint(cLMax/10,cLMax)

#Generate random numbers for start position
xPosRandom = np.random.randint(aRand,max(xRange)-aRand)         #This is to make sure the object stays within the confides of the image!
yPosRandom = np.random.randint(bRand,max(yRange)-bRand)


rRand = np.random.randint(cLMax/10,cLMax/5)
sphere = sphere.sphere("xs",0,0,0,xPosRandom,yPosRandom,cLMax,xRange,yRange,rRand)

#sphere.calcThicknessMatrix()

alphaRand = np.random.randint(0,90)
betaRand = np.random.randint(0,90)
gammaRand = np.random.randint(0,90)

#Random cuboid object
#cube = object.cuboid("cmj",0,0,0,xPosRandom,yPosRandom,cLMax,xRange,yRange,aRand,bRand,cRand)
#cube = object.cuboid("cmj",alphaRand,betaRand,gammaRand,xPosRandom,yPosRandom,50,xRange,yRange,aRand,bRand,cRand)



cube = cuboid.cuboid("cmj",0,0,0,50,50,50,xRange,yRange,20,20,20)



 
#plotting of STEM prototype (no noise yet)

#A = sphere.thicknessMatrix
B = cube.thicknessMatrix

            
addPoissonNoise(B)            
           
plt.pcolormesh(xRange, yRange, B, cmap="Greys_r")
#plt.show()
#plt.savefig('SimulationImages/Spheres/plot'+str(sys.argv[1])+'.png')     #sys.argv is the input from the bash script
plt.savefig('Cuboids/plot'+str(200)+'.png')     #sys.argv is the input from the bash script


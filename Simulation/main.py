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
from pyquaternion import Quaternion

sf = 1

#Let N be the number of events at each pixel, where the total is a constant. Or just keep N a factor? So as we jump from 128 to 256, sf = 2 from 1, then N per pixel will drop by 4. 
#To start off then, let's set N to 8 (so max we can go is 1024 -> 512 - > 256 -> 128)
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

def intersect_heights(p_arr,tri,r_arr):
    norm,v0,v1,v2 = tri
    u = v1-v0
    v = v2-v0
    d = r_arr         #This is the ray from the beam
    b = np.inner(norm,d)            #b==0 means n o intersection
    g = p_arr-v0            #Vector from every pixel to the vertex v0
    a = np.inner(norm,g)        #a factor
    h = -a/b
    ustar = np.cross(u, norm)
    vstar = np.cross(v, norm)
    c1 = np.inner((p_arr - v0 + (h*d.T).T), ustar)/np.inner(v, ustar)
    c2 = np.inner((p_arr - v0 + (h*d.T).T), vstar)/np.inner(u, vstar)
    h[(c1<0)+(c2<0)+(c1+c2>1)+(b==0)] = np.nan       #we can't let 0 - 0
    #Works out if intersection is within triangle
    return h


def calc_thickness_matrix(objects,n,dxdt,dydt,dxdr,dydr,pixel_size=1):       #n is scan points, a is pixel size
    a = np.arange(0,n)-n//2
    x,y = np.meshgrid(a*pixel_size, a*pixel_size)
    xr = np.zeros(n*n)
    yr = np.zeros(n*n)
    if dxdt != 0 or dydt != 0:
        t = np.arange(x.size)
        new_x = x.flatten() + t*dxdt
        y_mat = x.flatten() + t*dydt
        y_mat_transpose = y_mat.reshape(n,n).T
        new_y = y_mat_transpose.flatten()
        p_arr = np.stack([new_x, new_y, np.zeros(n*n)]).T
    else:
        p_arr = np.stack([x.flatten(),y.flatten(),np.zeros(n*n)]).T

    if dxdr != 0 or dydr != 0:
        tr = np.arange(xr.size)
        new_xr = xr + dxdr
        new_yr = yr + dydr
        yr_mat_t = new_yr.reshape(n,n).T
        new_yr = yr_mat_t.flatten()
        r_arr = np.stack([new_xr,new_yr,np.ones(n*n)]).T
        r_arr_sum = np.array([r_arr[:,0]**2+r_arr[:,1]**2+r_arr[:,2]**2]).T
        r_arr_new = r_arr/r_arr_sum
        #r_arr = r_arr_new
    else:
        r_arr = np.stack([xr.flatten(),yr.flatten(),np.ones(n*n)]).T

    #This takes all the pixels and displays the x,y,z locations as tuples. By definition, it's a 16384x3 matrix. Each of the pixels (16384) contains it's x, y and z coordinates.
    thick_array = np.zeros(p_arr.shape[0])
    for o in objects:       #for each of the individual objects
        planes = o.planes   #For cuboid there is 12 planes as I converted each plane to two triangles
        thickn = np.zeros((len(planes),p_arr.shape[0]))
        for k, tri in enumerate(planes):         #k is the iterator, t is the element within objects
            #print(tri)
            thickn[k,:] = intersect_heights(p_arr,tri,r_arr)
            u = thickn[k,:]
            z = u.reshape(n,n)
            
        thickness_mat = np.nanmax(thickn, axis=0)-np.nanmin(thickn, axis=0)
        where_are_NaNs = np.isnan(thickness_mat)
        thickness_mat[where_are_NaNs] = 0
        if o.deformation:
            thick_array -= thickness_mat            #Temporary for testing deformations
        else:
            thick_array += thickness_mat
    j = -np.sort(-thick_array)
    t_mat = thick_array.reshape(n,n)
    return t_mat





x_pixels, y_pixels = 128, 128		#128x128 pixels



xRange = [i for i in range(0,int(128*sf))]        #128x128 scan for probe, across 100x100
yRange = [i for i in range(0,int(128*sf))]
zRange = [i for i in range(0,int(128*sf))]


t0 = time.time()
for g in range(1):
    n = 128
    a = 1
    #Generating an test object, let a cube.

    #Generate random parameters of the cube
    aRand = np.random.randint(60*sf,70*sf)
    bRand = np.random.randint(60*sf,70*sf)
    cRand = np.random.randint(60*sf,70*sf)

    #Generate random numbers for start position
    xPosRandom = np.random.randint(-5*sf,5*sf)         #This is to make sure the object stays within the confides of the image!
    yPosRandom = np.random.randint(-5*sf,5*sf)          #Centered at between 45 and 55.


    #rRand = np.random.randint(cLMax/10,cLMax/5)
    #sphere = sphere.sphere("xs",False,0,0,0,xPosRandom,yPosRandom,cLMax,xRange,yRange,rRand)

    #sphere.calcThicknessMatrix()

    randomQuarternion = Quaternion.random()
    randomQuarternion = Quaternion(1,0,0,0)

    cube = cuboid.cuboid("cmj",False,randomQuarternion,xPosRandom,yPosRandom,0,xRange,yRange,aRand,bRand,cRand)
    #cube = cuboid.cuboid("cmj",False,0,0,0,50,50,50,xRange,yRange,30,35,40)
    #objects = [cube]
    objects=[cube]
    
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
        if int(sys.argv[2]) == 9:

            rand_int = random.randint(1,8)
            deformTheseCornersResult = random.sample(range(0,8),rand_int)
        else:
            deformTheseCornersResult = random.sample(range(0,8),int(sys.argv[2]))
        #print(deformTheseCornersResult)
    else:
        deformTheseCornersResult = []


    deforms = aD.addDeformation(cube,'cuboid',deformTheseCornersResult,sf)
    dA = deforms.deformArray

    #The deformations are tripyr which are created in this loop
    for i in range(len(dA)):
        deformation = tripyr.tripyr("xcl",True,randomQuarternion,xPosRandom,yPosRandom,0,xRange,yRange,dA[i][0],dA[i][1],dA[i][2],dA[i][3],cube.xAxis,cube.yAxis,cube.zAxis)
        objects.append(deformation)

    tSubZero = time.time()
    for i in range(len(objects)):           #We tell all the objects to rotate one by one
        objects[i].doRotation()

	#Need to use function to find the optimal area for the probe to operate. Does this interfere with the rotations while moving? If so how to fix. 
	#We can call the function once here as a preliminary, and call again during the loop?


    flatBackground = 20              #Flat background from the carbon layer. For now background will scale with scale factor
    image = (calc_thickness_matrix(objects,n,0,0,1,0) + flatBackground)               #Flat background and image will all scale with N, the number of electrons (dose) hitting the atom column
    #Adding gaussian blur
    gauss_blur = 1
    image = scipy.ndimage.filters.gaussian_filter(image,sigma=gauss_blur)

    np.asmatrix(image)
    #Adding poisson noise
    image = addPoissonNoise(image)
    plt.figure(figsize=(5,5))
    
    plt.pcolormesh(xRange, yRange, image, cmap="gray")
#print(image[34][34]-image[33][33])
#np.savetxt("debug.csv", image, delimiter=",")

    #plt.show()
    #print(time.time()-t0)
    #plt.savefig('SimulationImages/Spheres/plot'+str(sys.argv[i])+'.png')     #sys.argv is the input from the bash script
    #plt.savefig('/home/z/Documents/pics/1deform/image' + str(sys.argv[1]) + '.png', bbox_inches='tight', pad_inches = 0)     #sys.argv is the input from the bash script made for 1deform on linux rn
    #plt.imsave('/home/z/Documents/128ImagesBasic/' + str(sys.argv[3]) + '/test' + str(sys.argv[1]) + '.jpg',image,format='jpg',cmap = 'gray')
    #plt.imsave(str(sys.argv[3]) + '/test' + str(sys.argv[1]) + '.jpg',image,format='jpg',cmap = 'gray')
    # plt.savefig('~/Users/ziyuewang/Documents/Y4\ project/Presentations/rotate' + str(sys.argv[3]) + '.jpg')
    #plt.close()

	#Code for second image, bimodal
    newQuaternion = Quaternion.random()
    print(newQuaternion)
    for i in range(len(objects)):
        objects[i].randomQuarternion = newQuaternion
        objects[i].doRotation()

    image2 = (calc_thickness_matrix(objects,n,dxdt=0,dydt=0,dxdr=0,dydr=0) + flatBackground)
    image2 = scipy.ndimage.filters.gaussian_filter(image2,sigma=gauss_blur)
    np.asmatrix(image2)
    image2 = addPoissonNoise(image2)
    plt.figure(figsize=(5,5))
    plt.pcolormesh(xRange, yRange, image2, cmap="gray")
    plt.show()




	

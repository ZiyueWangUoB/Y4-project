# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 19:48:48 2018

@author: theisw
"""

import numpy as np
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt


np.seterr(all='ignore')

def intersect_heights(p_arr,tri):
    """ adapted from https://www.erikrotteveel.com/python/three-dimensional-ray-tracing-in-python/
    
    Parameters
    ==========
        p: arrays of poins, shape: 
    """
    #print(p_arr.shape, tri.shape)
    
    #p_arr is pixel array, 16384 x 3. 16384 = 128x128, meaning it's the flattened pixel matrix
    #Each pixel in the list (16384) has a tuple containing information about the locaiton of the pixel in 3D.
    #tri shape is 3x3
    #Pixel array displays the pixels 4 times???
    v2, v0, v1 = tri
    #Does the triangular based pyramid all at once. v2 has the four corners, and v2 itself is the first vertex. I.E v2 is the vertex, it's just run through four times as this function is called for each of the planes.
    u = v1 - v0
    v = v2 - v0
    normal = np.cross(u, v)
    d = np.array([[0,0,1]])     #vector for the STEM microscope beam.
    b = np.inner(normal, d)     # b == 0 means no intersection
    g = p_arr-v0
    print(g[0])
    #print(v0.shape)
    a = np.inner(normal, g)            #Figues out the height apparently, leave it.
    #print(a.shape)
    h = -a/b    # h is height
    # determine whether is inside
    #print(h.shape)
    ustar = np.cross(u, normal)
    vstar = np.cross(v, normal)    
    c1 = np.inner((p_arr - v0 + (h*d.T).T), ustar)/np.inner(v, ustar)
    c2 = np.inner((p_arr - v0 + (h*d.T).T), vstar)/np.inner(u, vstar)
    h[(c1<0)+(c2<0)+(c1+c2>1)+(b==0)] = np.nan    # + serves as OR in this context
    
    #How does this essentially differ from my code? The whole pixel array is inputed into this function, specifying the coordinates of each pixel as a tuple. The height is then worked out for each individual pixel location simultaniously. Then it's determined whether it is inside. This is looped over (for loop) for all the individual objects.
    return h
   
    

class Convex:
    """ defined by the inside of a surface made up of triangles 
    triangles is an array with shape (n,3,3), triang nr, corner nr, x/y/z
    """
    
    def __init__(self, triangles):
        self.triangles = triangles
        self.triangles_original = triangles.copy()
        
    def euler_rotate(self, theta_deg):
        """ rotates corners by euler angles
        """
        theta = np.deg2rad(np.array(theta_deg))
        R_x = np.array([[1, 0, 0],
                        [0, np.cos(theta[0]), -np.sin(theta[0])],
                        [0, np.sin(theta[0]), np.cos(theta[0])]])
        R_y = np.array([[np.cos(theta[1]), 0, np.sin(theta[1])],
                        [0, 1, 0],
                        [-np.sin(theta[1]), 0, np.cos(theta[1])]])
        R_z = np.array([[np.cos(theta[2]), -np.sin(theta[2]), 0],
                        [np.sin(theta[2]), np.cos(theta[2]), 0],
                        [0, 0, 1]])
        R = np.dot(R_z, np.dot( R_y, R_x))
        self.triangles = np.dot(self.triangles_original, R.T)
        
    def image(self, n, pix_size=1, noise=None, background=0, noisescale=0.01, gauss=None, dydt=0, dxdt=0):
        """ calculates thickness image """
        a = np.arange(0,n)-n//2
        x,y = np.meshgrid(a*pix_size,a*pix_size)
        if dxdt != 0 or dydt != 0:
            t = np.arange(x.size)
            p_arr = np.stack([x.flatten() + t*dxdt, y.flatten() + t*dydt, np.zeros(n*n)]).T
        #print(p_arr.shape)      #Flattens it so we have now 3x16384 matrix. Transposed so we go by pixel.
        else:
            print('fart')
            p_arr = np.stack([x.flatten(),y.flatten(),np.zeros(n*n)]).T
        th = self.thickness(p_arr) + background
        if gauss is not None:
            th = gaussian_filter(th, sigma=gauss)
        if noise is not None:
            th += noisescale * np.random.poisson(lam=noise*th)
        return th
        
    def thickness(self, p_arr):
        """ thickness along z direction """
        thickn = np.zeros((self.triangles.shape[0], p_arr.shape[0]))
        #Each triangle (first indent) has 3 vertexes with 3 cord for each vertex. 2nd indent is the vertex num. 3rd indent is cords x,y,z detail.
        #thickn is 4x16384 matrix detailing all the thickness matrix for each of the triangles.
        for k, t in enumerate(self.triangles):
            #print(k,t)
            #t is the 3x3 matrix for each of the triangles (contains info on vertex cords for each vertex) and k is the triangle number (4 triangles in total in this case)
            thickn[k,:] = intersect_heights(p_arr,t)                #Instead of giving the calc thickness one pixel at a time, It gives it the whole image and calculates it in one go???
        print(thickn.shape)
        t = np.nanmax(thickn, axis=0)-np.nanmin(thickn, axis=0)
        #t[np.isnan(t)] = 0
        if np.isnan(t):
            t = 0
        return t


if __name__ == '__main__':
            
    tri = np.array([[[0,0,0], [0,0,1], [0,1,0]],
                    [[0,0,0], [0,0,1], [1,0,0]],
                    [[0,0,0], [0,1,0], [1,0,0]],
                    [[0,0,1], [0,1,0], [1,0,0]]])
                    #All data points. each row is a plane, each tuple is a vertex. This is done for 4 planes of the triangular based pyramid.
                    
                    #triangular based pyramid has 4 edges shown here.
    '''
    cube = np.array([[[0,0,0], [1,0,0], [0,1,0]], # bottom
                     [[1,1,0], [1,0,0], [0,1,0]], 
                     [[0,0,1], [1,0,1], [0,1,1]], # top
                     [[1,1,1], [1,0,1], [0,1,1]],
                     [[0,0,0], [0,1,0], [0,0,1]], # permute ->
                     [[0,1,1], [0,1,0], [0,0,1]],
                     [[1,0,0], [1,1,0], [1,0,1]], # 
                     [[1,1,1], [1,1,0], [1,0,1]],
                     [[0,0,0], [0,0,1], [1,0,0]], # permute ->
                     [[1,0,1], [0,0,1], [1,0,0]],
                     [[0,1,0], [0,1,1], [1,1,0]], # 
                     [[1,1,1], [0,1,1], [1,1,0]]])-0.5+0.002
    '''
    n = 128 # scan points
    nr_rows, nr_cols = 4, 5
    # generate shape    
    t = Convex(tri)
    fig = plt.figure(figsize=(15, 10))
    for nr, r in enumerate(np.random.rand(nr_rows * nr_cols, 3)*360):
        #t.euler_rotate(r)
            #th = t.image(n, pix_size=2/n, noise=3, gauss=1.5, background=10)
        th = t.image(n, pix_size=2/n, noise=3, gauss=1.5, background=10, dxdt=2e-5)
        im = th.reshape(n,n)
        ax = fig.add_subplot(nr_rows, nr_cols, nr+1)
        ax.imshow(im, cmap='gray')








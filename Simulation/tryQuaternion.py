import numpy as np
from pyquaternion import Quaternion

corner = np.array([10,0,0])
q1 = Quaternion(axis=[0.5,1,0],angle=-3.14159265/2)
cornerPrime = q1.rotate(corner)
print(cornerPrime)
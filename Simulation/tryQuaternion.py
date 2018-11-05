import numpy as np
import math
from pyquaternion import Quaternion

corner = np.array([10,00,0])
q1 = Quaternion(axis=[0,-1,0],angle=90*math.pi/180)
cornerPrime = q1.rotate(corner)
#print(cornerPrime)

zeroNegative = -1.0
zeroPositive = 0.0

print(zeroNegative,zeroPositive)


def testBool():
    if zeroNegative == zeroPositive:
        print('floats equal to eachother')
        return True
    else:
        return False

if not testBool():
    print('it is true!')
        




import matplotlib.pyplot as plt
import numpy as np


x = ['0','=/= 0']
y = [95,95.8]

plt.scatter(x,y)
plt.xlabel('Number of deformations (0 or =/= 0)')
plt.ylabel('Test accuracy %')
plt.savefig('binary.eps')

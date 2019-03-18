import matplotlib.pyplot as plt
import numpy as np

deform = [i for i in range(9)]
test_acc = [93.9,56.7,55.8,40,53.7,52.0,41,71.1,94]

plt.scatter(deform,test_acc)
plt.xlabel('Number of deformations')
plt.ylabel('Test accuracy %')
#plt.savefig('deform.eps')




plt.figure()
test_acc_pm1 = [93.9,98.6,91.6,97.9,96.8,92.8,95.0,99,94]
plt.xlabel('Number of deformations ±1')
plt.ylabel('Test accuracy %')
#plt.xticks(['0','1,2','1,2,3','2,3,4','3,4,5','4,5,6','5,6,7','6,7','8'])
plt.scatter(deform,test_acc_pm1)
plt.savefig('deformPm12.eps')



'''
test_acc_pm1_all = [93.9,98.6,91.6,97.9,96.8,92.8,95.0,99,94]
plt.scatter(deform,test_acc_pm1_all)
plt.show()
'''

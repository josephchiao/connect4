import numpy as np
import os
import shutil
import matplotlib.pyplot as plt # type: ignore
import archive.theta_init as theta_init


thetas_0 = np.load('/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network Restructure/connect4/genetic_elite_data/nn_theta_set_0.npz')
theta_1 = thetas_0['Theta1']
theta_2 = thetas_0['Theta2']
theta_3 = thetas_0['Theta3']


print(np.shape(theta_1))
print(np.shape(theta_2))
print(np.shape(theta_3))



#np.savez('/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network Restructure/connect4/genetic_elite_data/nn_theta_set_0.npz', Theta1 = theta_1, Theta2 = theta_2, Theta3 = theta_3, b_2 = b_2, b_3 = b_3, b_output = b_output)



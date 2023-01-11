from math import comb
import numpy as np
import random

def point_mutaion(dataset, mutaion_rate):
    thetas = np.load(f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{dataset}.npz')
    theta_1 = thetas['Theta1'].flatten()
    theta_2 = thetas['Theta2'].flatten()
    theta_3 = thetas['Theta3'].flatten()
    combined_theta = np.concatenate((theta_1, theta_2, theta_3), axis = None)
    
    n = round(len(combined_theta) * mutaion_rate)
    mutations = [random.randint(0, len(combined_theta) - 1) for i in range(n)]
    for m in mutations:
        combined_theta[m] = np.random.normal(0, 1, 1)

    theta_1 = np.array(combined_theta[0:len(theta_1)]).reshape(thetas['Theta1'].shape)
    theta_2 = np.array(combined_theta[len(theta_1):(len(theta_1) + len(theta_2))]).reshape(thetas['Theta2'].shape)
    theta_3 = np.array(combined_theta[(len(theta_1) + len(theta_2)):(len(theta_1) + len(theta_2) + len(theta_3))]).reshape(thetas['Theta3'].shape)
    
    np.savez(f'/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network(Kai)/connect4/genetic_training_data/nn_theta_set_{dataset}.npz', Theta1 = theta_1, Theta2 = theta_2, Theta3 = theta_3)


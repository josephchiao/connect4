import numpy as np
import random

def basic_reproduction(theta_set_1, theta_set_2):
    print("reproducing between ", theta_set_1, " and ", theta_set_2)
    p1_thetas = np.load(f'/home/joseph/Desktop/Connect 4/connect4/genetic_parent_data/nn_theta_set_{theta_set_1}.npz')
    p1_theta_1 = p1_thetas['Theta1'].flatten()
    p1_theta_2 = p1_thetas['Theta2'].flatten()
    p1_theta_3 = p1_thetas['Theta3'].flatten()

    p2_thetas = np.load(f'/home/joseph/Desktop/Connect 4/connect4/genetic_parent_data/nn_theta_set_{theta_set_2}.npz')
    p2_theta_1 = p2_thetas['Theta1'].flatten()
    p2_theta_2 = p2_thetas['Theta2'].flatten()
    p2_theta_3 = p2_thetas['Theta3'].flatten()

    new_theta_1 = [random.randrange(0, 2) for i in range(len(p1_theta_1))]
    new_theta_2 = [random.randrange(0, 2) for i in range(len(p1_theta_2))]
    new_theta_3 = [random.randrange(0, 2) for i in range(len(p1_theta_3))]

    for i in range(len(new_theta_1)):
        if new_theta_1[i]:
            new_theta_1[i] = p1_theta_1[i]
        
        else:
            new_theta_1[i] = p2_theta_1[i]

    for i in range(len(new_theta_2)):
        
        if new_theta_2[i]:
            new_theta_2[i] = p1_theta_2[i]
        
        else:
            new_theta_2[i] = p2_theta_2[i]

    for i in range(len(new_theta_3)):
        
        if new_theta_3[i]:
            new_theta_3[i] = p1_theta_3[i]
        
        else:
            new_theta_3[i] = p2_theta_3[i]

    new_theta_1 = np.reshape(new_theta_1, (p1_thetas['Theta1'].shape))
    new_theta_2 = np.reshape(new_theta_2, (p1_thetas['Theta2'].shape))
    new_theta_3 = np.reshape(new_theta_3, (p1_thetas['Theta3'].shape))

    return(new_theta_1, new_theta_2, new_theta_3)

def multi_parent_reproduction(parent_sets):
    
    parent_set_count = len(parent_sets)
    parent_thetas = []
    
    for parent in parent_sets:
        thetas = np.load(f'/home/joseph/Desktop/Connect 4/connect4/genetic_parent_data/nn_theta_set_{parent}.npz')
        theta_1 = thetas['Theta1'].flatten()
        theta_2 = thetas['Theta2'].flatten()
        theta_3 = thetas['Theta3'].flatten()
        parent_thetas.append([theta_1 + theta_2 + theta_3])

    new_theta = [random.randrange(0, parent_set_count) for i in range(len(theta_1 + theta_2 + theta_3))]

    for i in range(len(new_theta)):
        new_theta[i] = parent_thetas[new_theta[i]][i]

    new_theta_1 = np.reshape(new_theta[0:len(theta_1)], thetas['Theta1'].shape)
    new_theta_2 = np.reshape(new_theta[len(theta_1):(len(theta_1) + len(theta_2))], thetas['Theta2'].shape)
    new_theta_3 = np.reshape(new_theta[(len(theta_1) + len(theta_2)):(len(theta_1) + len(theta_2) + len(theta_3))], thetas['Theta3'].shape)
    
    return(new_theta_1, new_theta_2, new_theta_3)
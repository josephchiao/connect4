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


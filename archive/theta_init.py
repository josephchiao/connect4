import numpy as np

def logistic_theta_init(loc, scale, size):

    return np.random.logistic(loc, scale, size)

def normal_theta_init(loc, scale, size):

    return np.random.normal(loc, scale, size)

def create_file(theta_1_size, theta_2_size, theta_3_size, b_2_dim, b_3_dim, b_output_dim, file_name = "nn_theta_set.npz", init_type = "normal"):

    if init_type == "logistic":
        theta_1 = logistic_theta_init(0, 1, theta_1_size)
        theta_2 = logistic_theta_init(0, 1, theta_2_size)
        theta_3 = logistic_theta_init(0, 1, theta_3_size)
        

    if init_type == "normal":
        theta_1 = normal_theta_init(0, 1, theta_1_size)
        theta_2 = normal_theta_init(0, 1, theta_2_size)
        theta_3 = normal_theta_init(0, 1, theta_3_size)
    
    b_2 = np.zeros((1, b_2_dim))
    b_3 = np.zeros((1, b_3_dim))
    b_output = np.zeros((1, b_output_dim))

    np.savez(file_name, Theta1 = theta_1, Theta2 = theta_2, Theta3 = theta_3, b_2 = b_2, b_3 = b_3, b_output = b_output)


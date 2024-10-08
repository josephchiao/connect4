import numpy as np
import time


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

def ReLU(x):
    return x * (x > 0)

def feedforward_prop(X, Theta1, Theta2, Theta3):

    X = np.hstack((1, X))

    a_2 = ReLU(X @ Theta1)

    a_2_flat = np.hstack((1, a_2))

    a_3 = sigmoid(a_2_flat @ Theta2)

    a_3_flat = np.hstack((1, a_3))

    output = sigmoid(a_3_flat @ Theta3)

    return output
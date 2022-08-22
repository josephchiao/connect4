import numpy as np
import time


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def feedforward_prop(X, Theta1, Theta2, Theta3):
    X = np.hstack((1, X))

    a_2 = sigmoid(X @ Theta1)

    a_2 = np.hstack((1, a_2))

    a_3 = sigmoid(a_2 @ Theta2)

    a_3 = np.hstack((1, a_3))

    return sigmoid(a_3 @ Theta3)

import numpy as np
import os
import shutil
import matplotlib.pyplot as plt # type: ignore
import archive.theta_init as theta_init

class NeuralNetwork:
    def __init__(self, X_dim = None, a_2_dim = None, a_3_dim = None, output_dim = None):
        self.X_dim = X_dim
        self.a_2_dim = a_2_dim
        self.a_3_dim = a_3_dim
        self.output_dim = output_dim

        # Initialize weights
        self.theta_1_dim = (self.X_dim, self.a_2_dim)
        self.theta_2_dim = (self.a_2_dim, self.a_3_dim)
        self.theta_3_dim = (self.a_3_dim, self.output_dim)

    def theta_generate(self, n):

        """For initializing training set"""

        folder = '/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network Restructure/connect4/test_folder'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        for dataset in range(n):
            theta_init.create_file(self.theta_1_dim, 
                                   self.theta_2_dim, 
                                   self.theta_3_dim,
                                   self.a_2_dim,
                                   self.a_3_dim,
                                   self.output_dim, 
                                   file_name = f"/Users/joseph_chiao/Desktop/Advance Research/Machine Learning/Connect 4 Neural network Restructure/connect4/test_folder/nn_theta_set_{dataset}.npz", ## Fix formating
                                   init_type = "logistic")

    def theta_recover(self, location):

        thetas = np.load(location)
        self.theta_1 = thetas['Theta1']
        self.theta_2 = thetas['Theta2']
        self.theta_3 = thetas['Theta3']

        self.b_2 = thetas['b_2']
        self.b_3 = thetas['b_3']
        self.b_output = thetas['b_output']

    def theta_single_use(self):
        
        self.theta_1 = theta_init.logistic_theta_init(0, 1, self.theta_1_dim)
        self.theta_2 = theta_init.logistic_theta_init(0, 1, self.theta_2_dim)
        self.theta_3 = theta_init.logistic_theta_init(0, 1, self.theta_3_dim)
        # Initialize the biases
        self.b_2 = np.zeros((1, self.a_2_dim))
        self.b_3 = np.zeros((1, self.a_3_dim))
        self.b_output = np.zeros((1, self.output_dim))

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def ReLU(x):
        return x * (x > 0)

    def ReLU_derivative(x):
        return 1 * (x > 0)

    def feedforward(self, X):
        
        # Input to a_2
        self.hidden_a_2 = np.dot(X, self.theta_1) + self.b_2
        self.a_2 = self.sigmoid(self.hidden_a_2)

        # a_2 to a_3
        self.hidden_a_3 = np.dot(self.a_2, self.theta_2) + self.b_3
        self.a_3 = self.sigmoid(self.hidden_a_3)

        # a_3 to output
        self.hidden_output = np.dot(self.a_3, self.theta_3) + self.b_output
        self.output = self.sigmoid(self.hidden_output)
        return self.output

    def backward(self, X, y, learning_rate):
        # Compute the output layer error
        output_error = y - self.output
        output_delta = output_error * self.sigmoid_derivative(self.output)

        # Compute the a_3 layer error
        a_3_error = np.dot(output_delta, self.theta_3.T)
        a_3_delta = a_3_error * self.sigmoid_derivative(self.a_3)

        # Compute the a_2 layer error
        a_2_error = np.dot(a_3_delta, self.theta_2.T)
        a_2_delta = a_2_error * self.sigmoid_derivative(self.a_2)


        # Update weights and biases
        self.theta_3 += np.dot(self.a_3.T, output_delta) * learning_rate
        self.b_output += np.sum(output_delta, axis=0, keepdims=True) * learning_rate

        print(np.shape(self.a_3.T), np.shape(output_delta))
        print(np.shape(self.theta_3))
        self.theta_2 += np.dot(self.a_2.T, a_3_delta) * learning_rate
        self.b_3 += np.sum(a_3_delta, axis=0, keepdims=True) * learning_rate

        self.theta_1 += np.dot(X.T, a_2_delta) * learning_rate
        self.b_2 += np.sum(a_2_delta, axis=0, keepdims=True) * learning_rate

    def softmax(self, temperature = 1, axis = None):

        beta = 1 / (temperature)
        x_max = np.amax(self.output, axis=axis, keepdims=True)
        exp_x_shifted = np.exp(beta * (self.output - x_max))
        return (exp_x_shifted / np.sum(exp_x_shifted, axis=axis, keepdims=True))

    def train(self, X, y, epochs, learning_rate):
        for epoch in range(epochs):
            output = self.feedforward(X)
            self.backward(X, y, learning_rate)
            if epoch % 4000 == 0:
                loss = np.mean(np.square(y - output))
                print(f'Epoch {epoch}, Loss:{loss}')
import numpy as np


class NeuralNetwork(object):
    def __init__(self, input_nodes, hidden_nodes, output_nodes, learning_rate):
        # Set number of nodes in input, hidden and output layers.
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        # Initialize weights
        self.weights_input_to_hidden = np.random.normal(0.0, self.input_nodes**-0.5, 
                                       (self.input_nodes, self.hidden_nodes))
        
        # Print input to hidden weights
        # print(self.weights_input_to_hidden)
        
        # Print shape of input to hidden weights
        # print(self.weights_input_to_hidden.shape)

        self.weights_hidden_to_output = np.random.normal(0.0, self.hidden_nodes**-0.5, 
                                       (self.hidden_nodes, self.output_nodes))
        
        # Print hidden to output weights
        # print(self.weights_hidden_to_output)
        
        # Print hidden to output shape
        # print(self.weights_hidden_to_output.shape)
        
        # Initialize learning rate
        self.lr = learning_rate
        
        # Define activation function
        def sigmoid(x):
           return 1 / (1 + np.exp(-x))
        self.activation_function = sigmoid
                    

    def train(self, features, targets):
        ''' Train the network on batch of features and targets. 
        
            Arguments
            ---------
            
            features: 2D array, each row is one data record, each column is a feature
            targets: 1D array of target values
        
        '''
        n_records = features.shape[0]
        delta_weights_i_h = np.zeros(self.weights_input_to_hidden.shape)
        delta_weights_h_o = np.zeros(self.weights_hidden_to_output.shape)
        for X, y in zip(features, targets):
            # Obtain output via forward pass
            final_outputs, hidden_outputs = self.forward_pass_train(X)
            
            # Back propagate to obtain error term
            delta_weights_i_h, delta_weights_h_o = self.backpropagation(final_outputs, hidden_outputs, X, y, 
                                                                        delta_weights_i_h, delta_weights_h_o)
        # Update the change in weights
        self.update_weights(delta_weights_i_h, delta_weights_h_o, n_records)


    def forward_pass_train(self, X):
        ''' 
        Implement forward pass here 
         
        Arguments
        ---------
        X: features batch
        '''
        #### Implement the forward pass here ####
        ### Forward pass ###
        # Done: Hidden layer - Replace these values with your calculations.
        hidden_inputs = np.dot(X, self.weights_input_to_hidden) # signals into hidden layer
        
        # Hidden output shape = (1, 2)
        hidden_outputs = self.activation_function(hidden_inputs)
#         print("Hidden Output shape:", hidden_outputs.shape)

        # Done: Output layer - Replace these values with your calculations.
        final_inputs = np.dot(hidden_outputs, self.weights_hidden_to_output)
        # Output layer shape = (1,)
        final_outputs = final_inputs # signals from final output layer
#         print("Final Output shape:", final_outputs.shape)
        
        return final_outputs, hidden_outputs

    def backpropagation(self, final_outputs, hidden_outputs, X, y, delta_weights_i_h, delta_weights_h_o):
        ''' Implement backpropagation
         
            Arguments
            ---------
            final_outputs: output from forward pass
            y: target (i.e. label) batch
            delta_weights_i_h: change in weights from input to hidden layers
            delta_weights_h_o: change in weights from hidden to output layers

        '''
        #### Implement the backward pass here ####
        ### Backward pass ###

        # Done: Output error - Replace this value with your calculations.
        error = y - final_outputs # Output layer error is the difference between desired target and actual output.
        
        # Since no activation function was used, the error term would be the error multiplied by one.
        output_error_term = error * 1
        
        # Done: Calculate the hidden layer's contribution to the error
        hidden_error = np.dot(self.weights_hidden_to_output, output_error_term)
        
        # Sigmoid function error term calculation
        hidden_error_term = hidden_error * hidden_outputs * (1 - hidden_outputs)
        
        # Hidden_error_term = (2, 1) X = 1, 3
        delta_weights_i_h += X[:, None] * hidden_error_term[None, :] 
        # Weight step (hidden to output)
        delta_weights_h_o += hidden_outputs[:, None] * output_error_term
        
        return delta_weights_i_h, delta_weights_h_o

    def update_weights(self, delta_weights_i_h, delta_weights_h_o, n_records):
        ''' Update weights on gradient descent step
         
            Arguments
            ---------
            delta_weights_i_h: change in weights from input to hidden layers
            delta_weights_h_o: change in weights from hidden to output layers
            n_records: number of records

        '''
        self.weights_hidden_to_output += self.lr * delta_weights_h_o / n_records 
        self.weights_input_to_hidden += self.lr * delta_weights_i_h / n_records 

    def run(self, features):
        ''' Run a forward pass through the network with input features 
        
            Arguments
            ---------
            features: 1D array of feature values
        '''
        
        #### Implement the forward pass here ####
        # TODO: Hidden layer - replace these values with the appropriate calculations.
        hidden_inputs = np.dot(features, self.weights_input_to_hidden) # signals into hidden layer
        hidden_outputs = self.activation_function(hidden_inputs) # signals from hidden layer
        
        # TODO: Output layer - Replace these values with the appropriate calculations.
        final_inputs = np.dot(hidden_outputs, self.weights_hidden_to_output) # signals into final output layer
        final_outputs = final_inputs # signals from final output layer 
        
        return final_outputs


#########################################################
# Set your hyperparameters here
##########################################################
iterations = 3000
learning_rate = 0.5
hidden_nodes = 10
output_nodes = 1

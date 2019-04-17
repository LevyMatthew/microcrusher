# Load libraries
import numpy as np
from keras import models
from keras import layers
from keras.utils import to_categorical


np.random.seed(0)


#each input is a dict
#{holeAn:int holeAs holeBn position:int cost_to_call:int}
#input_data is a list of dicts
def interpret_input_data(input_data):
    return np.array([[0, 0, 0],[1, 1, 1]])
    
train_features = []

#each target is a vector (list) of floats (0-1)
#[p(fold), p(call), p(raise1x), p(raise2x), p(raise3x)]
train_target_vector = []

# Set the number of features we want
number_of_features = 5000

# Load feature and target data
#(train_features, train_target_vector), (test_features, test_target_vector) = load_data()
def train_model(features,target):
    # Start neural network
    model = models.Sequential()
    
    # Add fully connected layer with a ReLU activation function
    model.add(layers.Dense(32, input_dim=features.shape[-1], activation='relu'))
    
    # Add fully connected layer with a ReLU activation function
    model.add(layers.Dense(32, input_dim=32, activation='relu'))
    
    # Add fully connected layer with a softmax activation function
    model.add(layers.Dense(units=target.shape[-1], activation='softmax'))
    
    # Compile neural network
    model.compile(loss='sparse_categorical_crossentropy', # Cross-entropy
                    optimizer='rmsprop', # Root Mean Square Propagation
                    metrics=['accuracy']) # Accuracy performance metric
                    
    # Train neural network
    history = model.fit(features, # Features
                        target, # Target vector
                        epochs=3, # Three epochs
                        verbose=0, # No output
                        batch_size=20) # Number of observations per batch
    
    #validation_data=model.evaluate(test_features, test_target)
    
    return model
    
m = train_model(np.zeros((20,5)),np.zeros((20,1)))
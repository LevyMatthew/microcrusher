# Load libraries
from keras import models
from keras import layers

# Set the number of features we want
number_of_features = 5000

# Load feature and target data
#(train_features, train_target_vector), (test_features, test_target_vector) = load_data()

# Start neural network
network = models.Sequential()

# Add fully connected layer with a ReLU activation function
network.add(layers.Dense(units=100, activation='relu', input_shape=(number_of_features,)))

# Add fully connected layer with a ReLU activation function
network.add(layers.Dense(units=100, activation='relu'))

# Add fully connected layer with a softmax activation function
network.add(layers.Dense(units=46, activation='softmax'))

# Compile neural network
network.compile(loss='categorical_crossentropy', # Cross-entropy
                optimizer='rmsprop', # Root Mean Square Propagation
                metrics=['accuracy']) # Accuracy performance metric
                
# Train neural network
history = network.fit(train_features, # Features
                      train_target, # Target vector
                      epochs=3, # Three epochs
                      verbose=0, # No output
                      batch_size=100, # Number of observations per batch
                      validation_data=(test_features, test_target)) # Data to use for evaluation
import numpy as np

from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
from keras import models
from keras import layers
from keras.utils import to_categorical
from handhistory import *
NB_SIMULATION = 20

#Artificially intelligent Agent that attempts to model the behaviour of a small-
#stakes online poker player.
class SmallStakesPlayer(BasePokerPlayer):  # Do not forget to make parent class as "BasePokerPlayer"

    #  we define the logic to make an action through this method. (so this method would be the core of your AI)
    def declare_action(self, valid_actions, hole_card, round_state):
        community_card = round_state['community_card']
        self.win_rate = self.calculate_win_rate(hole_card,community_card)
                
        #Call
        if self.win_rate >= 1.0 / self.player_num:
            action = valid_actions[1]  # fetch CALL action info
        else: #Fold
            action = valid_actions[0]  # fetch FOLD action info
        return action['action'], action['amount']


    def receive_game_start_message(self, game_info): 
        print('Game Info:',game_info)
        #Count the amount of players                
        self.players = game_info['seats']
        self.player_num = game_info['player_num']
        rule = game_info['rule']
        self.sb = rule['small_blind_amount']

    def receive_round_start_message(self, round_count, hole_card, seats):
        self.hole_card = hole_card
        self.players = seats
        #self.player_num = len(seats)
        
    def receive_street_start_message(self, street, round_state):
        print('Street:',street)
        print('Round State:',round_state)
        community_card = round_state['community_card']
        self.hand = Hand(self.hole_card,community_card)
        #print('Hole Card',self.hole_card,':',type(self.hole_card))
        #print('Community Card',community_card,':',type(community_card))
        print('Hand:',self.hand)
        #self.win_rate = self.calculate_win_rate(self.hole_card,community_card)

    def receive_game_update_message(self, action, round_state):
        print('Action:',action)

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

    
    def calculate_win_rate(self,hole_card,community_card):
        return estimate_hole_card_win_rate(
                nb_simulation=NB_SIMULATION,
                nb_player=self.player_num,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )
        
    
    def input_vector(self):
        result = []
        result.append(self.win_rate) #first feature: win rate with current hand
        #TODO: Add more features:
        # Cost to call
        # position
        # is_dealer
        # is_bb
        # is_sb, 
        return result
        
#np.random.seed(0)

train_features = []

#each target is a vector (list) of floats (0-1)
#[p(fold), p(call), p(raise1x), p(raise2x), p(raise3x)]
train_target_vector = []

# Set the number of features we want
N_FEATURES = 1
BATCH_SIZE = 20

#each input is a dict
#{holeAn:int holeAs holeBn position:int cost_to_call:int}
#input_data is a list of dicts
def interpret_input_data(game_info):
    print(game_info)
    return np.zeros((BATCH_SIZE, N_FEATURES))


# Load feature and target data
#(train_features, train_target_vector), (test_features, test_target_vector) = load_data()
def train_model(features,target):
    # Start neural network
    model = models.Sequential()
    
    # Add fully connected layer with a ReLU activation function
    model.add(layers.Dense(32, input_dim=features.shape[-1], activation='sigmoid'))
    
    # Add fully connected layer with a ReLU activation function
    model.add(layers.Dense(32, input_dim=32, activation='sigmoid'))
    
    # Add fully connected layer with a softmax activation function
    model.add(layers.Dense(units=target.shape[-1], activation='sigmoid'))
    
    # Compile neural network
    model.compile(loss='kullback_leibler_divergence', # Cross-entropy
                    optimizer='rmsprop', # Root Mean Square Propagation
                    metrics=['accuracy']) # Accuracy performance metric
                    
    # Train neural network
    history = model.fit(features, # Features
                        target, # Target vector
                        epochs=100, # Three epochs
                        verbose=0, # No output
                        batch_size=BATCH_SIZE) # Number of observations per batch
                        
    
    #validation_data=model.evaluate(test_features, test_target)
    
    return model
    
#m = train_model(np.random.sample(N_FEATURES*BATCH_SIZE).reshape((BATCH_SIZE,N_FEATURES)),np.random.sample(BATCH_SIZE).reshape((BATCH_SIZE,1)))

def setup_ai():
    return SmallStakesPlayer()

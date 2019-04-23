from player import Player
from street import Street
from hand import Hand
from card import Card

#A round holds hand data and betting data
#Holds information about how people behave at certain stakes
#At zone poker, every person should be assumed to be painstakingly average
class Round(object):
    
    def __init__(self,lines):
        
        #Initial line describing whether it's a tournament, stakes, etc
        self.game_type = lines[0]
        #int - Number of players
        self.player_count = 0

        #Player[] all the involved players
        self.players = []        

        #All the involved players indexed by position
        self.player_at = {}

        self.board = [] #list of Card [3-5]
        self.player_hands = [] #list of Hands
        
        #HOLE, FLOP, TURN, RIVER, SUMMARY
        self.subheader_locs = []     
        self.streets = []
        street_names = ['HOLE','FLOP','TURN','RIVER','SUMMARY']
        self.street_by_name = {}
        
        #Count the Players and process position and stack information
        while lines[self.player_count+1][0:4] == 'Seat':
            
            #Starting at line 1, one line per player indicating: Seat, Position, Stack  
            self.player_count = self.player_count + 1
            words = lines[self.player_count].split(' ')
            
            seat = int(words[1][:-1])
            
            position = ''.join(words[2:-3])
            
            stack = lines[self.player_count].split('(')[1] #str
            stack = float(words[-3][1:].replace(',','').replace('$',''))
            
            p = Player(seat, position, stack)
            self.player_at[position] = p
            self.players.append(p)
            
            
        
                
        for index,line in enumerate(lines):
             
            #Subheader Line
            if line.split(' ')[0]=='***':
                word = line.split(' ')[1] #Word between the *** WORD ***  
                self.subheader_locs.append(index)
        
        for player in range(self.player_count):
            #Read Dealt Cards
            index = self.subheader_locs[0] + player + 1
            hand_str = lines[index][-8:-3]
            h = Hand(hand_str,self.board)
            self.players[player].hand = h
            self.player_hands.append(h)
        
        #TODO: Instances of Street for each street. Parse individual lines in street constructor
        for i,(begin,end) in enumerate(zip(self.subheader_locs[0:-1],self.subheader_locs[1:])):
            self.streets.append(Street(lines[begin:end]))
        # Read Preflop behaviour        
        # index = self.subheader_locs[0] + self.player_count + 1
        # line = lines[index]
        # stage = 'Pre-Flop'
        # while '***' not in line:
        #     words = line.split(' : ')            
        #     position = words[0]
        #     action = words[1]
        #     self.player_at[position.replace(' ','')].actions.append((stage,action))
        #     
        #     index = index + 1
        #     line = lines[index]
        # 
        # 
        # if self.has_flop:
        #     #Read Flop Cards
        #     index = self.subheader_locs[1]
        #     board_str = lines[index][-10:-2]
        #     self.board = [Card(i) for i in board_str.split(' ')]            
        #     
        # if self.has_turn:
        #     #Read Turn Card
        #     index = self.subheader_locs[2]
        #     turn_card = lines[index][-4:-2]
        #     self.board.append(Card(turn_card))
        #     
        # if self.has_river:
        #     #Read River Card
        #     index = self.subheader_locs[3]
        #     river_card = lines[index][-4:-2]
        #     self.board.append(Card(river_card))

       ##   self.player_results = ['']*self.player_count
        # for player in range(self.player_count):            
        #     index = self.subheader_locs[4] + player + 3
        #     if index < len(lines):
        #         self.player_results[player] = lines[index][8:]
        
        #self.players_in_flop = 
        #self.players_in_turn =       
        #self.final_pot_size = 
        
    #return list of floats 0-1 representing features based on round data
    def get_features(self):
        #pot odds
        #outs
        #if outs*0.02 > pot odds
        pass

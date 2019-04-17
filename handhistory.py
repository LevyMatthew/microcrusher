from os import listdir
from os.path import isfile, join
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt

hand_files = [f for f in listdir('hands') if isfile(join('hands',f))]

#Single card with suit and rank
class Card(object):    
    #2 is lowest, A is highest
    R = '23456789TJQKA'
    #spade, club, heart, diamond
    S = 'schd'    
    
    def __init__(self,card_str):
        if type(card_str) == str:       
            self.card_str = card_str
            
            #N = value of cards. 0 for 2, 12 for A
            self.r = Card.to_rank(card_str[0])
            
            #S = suit. S0,C1,H2,D3               
            self.s = Card.to_suit(card_str[1])        
            
    
    def __str__(self):
        return self.card_str
            
    
    def to_rank(r_str):
        return Card.R.index(r_str)
            
    def to_suit(s_str):
        return Card.S.index(s_str)


    __repr__ = __str__
#Set of two through seven cards with relative strengths
#Two of the cards are identified as pocket cards. The rest are board cards.
#The distinction matters. For example, AA in my pocket is usually better than
#AA on the board.
class Hand(object):
    
    #Pocket is kept separate from board cards because this affects relative hand strength
    #In the case where the hand is a set of 5 whose quality is being determined, pocket could be an empty list
    def __init__(self,pocket,board):
        self.pocket = []
        self.board = []
        if type(pocket) == str and len(pocket) > 0:
            self.pocket = [Card(card_str) for card_str in
 pocket.split(' ')]
        if type(board) == str and len(board) > 0:
            self.board = [Card(card_str) for card_str in board.split(' ')]

        #list of five cards
        self.cards = self.pocket + self.board
        self.ranks = [card.r for card in self.cards]
        self.suits = [card.s for card in self.cards]
    
    def __str__(self):
        return (' ').join([str(card) for card in self.cards])
    
    def made_hand(self):        
        h = {}
        q = self.made_hand_components()        
        if len(q['flush']) > 0 and len(q['straight']) > 0:
            pass
        elif len(q['flush']) > 0:
            pass
        elif len(q['straight']) > 0:
            pass
        #go through pair, set, two pair, etc replacing name and rank if exists 
        else:
            h['name'] = 'high card'
            h['rank'] = max(q['ranks'])
        return h
    
    #Return the hand, signifying any pairs, flushes, straights etc regardless of
    #whether they have been beaten
    def made_hand_components(self):
        q = {}
        #ranks of all cards in order
        q['ranks'] = sorted(self.ranks)  
        q['suits'] = sorted(self.suits)      
        #numerical value of pair 0 to 12. -1 for dne
        q['pocket pair'] = self.pocket[0].r*(self.pocket[0].r == self.pocket[1].r)
        q['pocket suited'] = (self.pocket[0].s == self.pocket[1].s)
        
        if len(self.board) > 0:
            #dictonary of lists of numerical value of multijple 0 to 12. [] for dne
            q['pair'] = self.get_pairs()        
            q['set'] = self.get_sets()
            q['quads'] = self.get_quads()
            
            q['straight']  = self.get_straights()
            q['flush'] = self.get_flushes()    
            #The above are all that is required to determine hand rank.
            #For example, a pair and a set make a full house
                
        return q
    
    #pairs are a combination of:
    #pocket pair
    #semi-pocket pair
    #board pair
    def get_pairs(self):
        #Entries in p are (r,k) where r is the rank and k is the number of hole cards used
        p = []
      

        #Pocket pair
        if self.ranks[0] == self.ranks[1]:
            p.append((self.ranks[0],2))
        else:
            #Semipocket pair - half board, half pocket
            for cardA in self.pocket:
                for cardB in self.board:
                    if cardA.r == cardB.r:
                        p.append((cardA.r,1))
                
        #Board pair
        for i,cardA in enumerate(self.board):
            for cardB in self.board[i+1:]:
                if cardA.r == cardB.r:
                    p.append((cardA.r,0))
                    
        return p
    
    def get_sets(self):
        s = []
        if self.ranks[0] == self.ranks[1]:
            for card in self.board:
                if card.r == self.ranks[0]:
                    s.append((card.r,2))
        else:
            for cardA in self.pocket:
                for i,cardB in enumerate(self.board):
                    if cardA.r == cardB.r:
                        for cardC in self.board[i+1:]:
                            if cardA.r == cardC.r:
                                s.append((cardA.r,1))
 
        for i,cardA in enumerate(self.board):
            for j,cardB in enumerate(self.board[i+1:]):
                if cardA.r == cardB.r:
                    for cardC in self.board[j+2:]:
                        if cardA.r == cardC.r:
                            s.append((cardA.r,0))                            
        return s
    
    #TODO
    def get_quads(self):
        return []
    
    def get_straights(self):
        s = []
        all_straights = [12]+list(range(13))
        
        for start in range(10):
            hole_cards = 0
            for i in range(5):
                if all_straights[start+i] not in self.ranks:                    
                    break
                elif all_straights[start+i] in [card.r for card in self.pocket]:
                    hole_cards = hole_cards + 1
            else:
                s.append((start+i,hole_cards))                    
        return s        
        
    #get full flushes
    def get_flushes(self):
        f = []
        for suit in range(4):
            hole_cards = 0
            if self.suits.count(suit) == 5:
                flush_cards = tuple(sorted(self.ranks)[:-5:-1])
                for i in self.pocket:
                    if i.s == suit and i.r in flush_cards:
                        hole_cards = hole_cards + 1
                f.append((flush_cards,hole_cards))
        return f
    
    def draws(self):
        pass
        
    __repr__ = __str__

class Player(object):
    
    def __init__(self, seat, position, stack):
        self.seat = seat
        self.position = position
        self.stack = stack
        self.actions = []
    

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
        self.subheader_locs = [-1]*5
        self.has_flop = False
        self.has_turn = False
        self.has_river = False
        
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
                #Process hole cards             
                if word == 'HOLE':
                    self.subheader_locs[0] = index                                    
                #Process flop cards
                elif word == 'FLOP':
                    self.subheader_locs[1] = index  
                    self.has_flop = True                                  
                elif word == 'TURN':
                    self.subheader_locs[2] = index
                    self.has_turn = True
                elif word == 'RIVER':
                    self.subheader_locs[3] = index
                    self.has_river = True
                elif word == 'SUMMARY':
                    self.subheader_locs[4] = index
        
        for player in range(self.player_count):
            #Read Dealt Cards
            index = self.subheader_locs[0] + player + 1
            hand_str = lines[index][-8:-3]
            h = Hand(hand_str,self.board)
            self.players[player].hand = h
            self.player_hands.append(h)
            #self.player_holes.append([Card(i) for i in hand_str.split(' ')])
        
        # Read Preflop behaviour
        index = self.subheader_locs[0] + self.player_count + 1
        line = lines[index]
        stage = 'Pre-Flop'    
        while '***' not in line:
            words = line.split(' : ')            
            position = words[0]
            action = words[1]
            self.player_at[position.replace(' ','')].actions.append((stage,action))
            
            index = index + 1
            line = lines[index]
 
        if self.has_flop:
            #Read Flop Cards
            index = self.subheader_locs[1]
            board_str = lines[index][-10:-2]
            print('FLOP: ' + board_str)
            self.board = [Card(i) for i in board_str.split(' ')]            
            
        if self.has_turn:
            #Read Turn Card
            index = self.subheader_locs[2]
            turn_card = lines[index][-4:-2]
            print('TURN: '+ turn_card)
            self.board.append(Card(turn_card))
            
        if self.has_river:
            #Read River Card
            index = self.subheader_locs[3]
            river_card = lines[index][-4:-2]
            print('RIVER: ' + river_card)
            self.board.append(Card(river_card))

        self.player_results = ['']*self.player_count
        for player in range(self.player_count):            
            index = self.subheader_locs[4] + player + 3
            if index < len(lines):
                self.player_results[player] = lines[index][8:]
        
        #self.players_in_flop = 
        #self.players_in_turn =       
        #self.final_pot_size = 
    
    
#File Input
def filter_lines(lines):
    
    forbidden = ['Table enter user', 'Table leave user', 'Draw for dealer', 'Enter(Auto)', 'Leave(Auto)', 'Table deposit','Seat sit out', 'Seat stand', 'Seat re-join']
    filtered = lines
    for f in forbidden:
        filtered = [i for i in filtered if f not in i]
    return filtered


#Scrape data from entire file from hands directory with name hand_file
def read_hand_file(hand_file):
    file = open('hands/'+hand_file)
    lines = file.readlines()
    file.close()
    lines = filter_lines(lines)
    
    #locate starts of hands
    round_start_locs = []
    
    #extract information from hands
    for index,line in enumerate(lines):
        if line[0:5] == 'Bodog':
           round_start_locs.append(index)
    
    #slice lines from file into individual roundl line sets
    round_lines_arr = []
    for index,start_loc in enumerate(round_start_locs[:-1]):
        round_lines_arr.append(lines[start_loc:round_start_locs[index+1]])
        
    #Process round lines into Round objects
    rounds = []
    for round_lines in round_lines_arr:
        rounds.append(Round(round_lines))        
    return rounds


#plot a heatmap of frequency for a set of hands preflop
def plot_hole_frequency(hands):
    buckets = np.zeros((13,13))
    for hand in hands:
        r = sorted(hand.ranks)
        print(r)
        s = hand.suits
        suited = (s[0] == s[1])
        pair = (r[0] == r[1])
        if suited:
            buckets[r[0]][r[1]] = buckets[r[0]][r[1]] + 1
        else:
            buckets[r[1]][r[0]] = buckets[r[1]][r[0]] + 1
    plt.imshow(buckets, cmap='hot', interpolation='nearest')
    plt.show()
    return buckets
    
def flop_filter(rounds):
    result = []
    for round in rounds:
        for player in round.players:
            if ('Pre-Flop','Folds\n') not in player.actions:
               result.append(player.hand)
    return result
                 
    
def save_holes_to_file(rounds):
    file = open('scraped_hands.txt','w+')
    for round in rounds:
         for i in range(round.player_count):
             file.write(str(round.player_holes[i])+' '+str(round.player_results[i])+'\n')
    file.close()
    
rounds = []
for hand_file in hand_files:    
    rounds.extend(read_hand_file(hand_file))

hands = []
for round in rounds:
    hands.extend(round.player_hands)
hands = flop_filter(rounds)

#Individual Hand Analysis
#h = Hand('9d Qs','As Ts Js Kc')
#print(h)
#print(h.made_hand_components())
#print(h.made_hand())

#hand_arr = [Hand('As Ad','') for i in range(10)]
    
#print(plot_hole_frequency(hands))
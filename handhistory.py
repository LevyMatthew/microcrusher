from os import listdir
from os.path import isfile, join
from itertools import combinations
import numpy as np
import matplotlib.pyplot as plt

from round import Round
from player import Player
from hand import Hand
from card import Card

#from smallstakes_player import SmallStakesPlayer

hand_files = [f for f in listdir('hands') if isfile(join('hands',f))]

    
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

#go through all rounds returning only the hands that saw the flop
def flop_filter(rounds):
    result = []
    for round in rounds:
        for player in round.players:
            if ('Pre-Flop','Folds\n') not in player.actions:
               result.append(player.hand)
    return result
                 
#data scraping hole cards and results from hands
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
    
print(plot_hole_frequency(hands))

#player = SmallStakesPlayer()

h = Hand(['H4','S4'],['D7','C3','S8'])
print(h)
print(h.made_hand_components())
print(h.best_made_hand())

h = Hand(['H4','S4'],['C4','H7','H8'])
print(h)
print(h.made_hand_components())
print(h.best_made_hand())

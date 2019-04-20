from card import Card

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
            
        if type(pocket) == list and len(pocket) > 0:
            self.pocket = [Card(card_str) for card_str in pocket]
        if type(board) == list and len(board) > 0:
            self.board = [Card(card_str) for card_str in board]

        #list of five cards
        self.cards = self.pocket + self.board
        self.ranks = [card.r for card in self.cards]
        self.suits = [card.s for card in self.cards]
    
    def __str__(self):
        return (' ').join([str(card) for card in self.cards])
    
    def best_made_hand(self): 
        h = {}
        q = self.made_hand_components()
        
        if len(self.board) > 0:
            if len(q['flush']) > 0 and len(q['straight']) > 0:
                straight_top_ranks = sorted([i[0] for i in q['straight']])[::-1]
                flush_ranks = []
                for i in q['flush']:
                    flush_ranks = flush_ranks + list(i[0])
                for top_rank in straight_top_ranks:
                    straight_ranks = range(top_rank-4,top_rank)
                    for rank in straight_ranks:
                        if rank not in flush_ranks:
                            break
                    else:
                        h['name'] = 'straightflush'
                        h['rank'] = top_rank
            #quads
            elif len(q['quad']) > 0:
                h['name'] = 'quad'
                h['rank'] = q['quad'][0]           
            #full house
            elif len(q['set']) > 0 and len(q['pair']) > 1:
                set_r = max(set)
                pair_r = max([i for i in q['pair'] if set_r != i])
            elif len(q['flush']) > 0:
                top_flush_r = max([max(i[0]) for i in q['flush']])
                h['name'] = 'flush'
                h['rank'] = top_flush_r
            elif len(q['straight']) > 0:
                top_straight_r = max([i[0] for i in q['straight']])
                h['name'] = 'straight'
                h['rank'] = top_straight_r
            #set
            elif len(q['set']) > 0:
                h['name'] = 'set'
                h['rank'] = max(q['set'])
            #twopair
            elif len(q['pair']) > 1:   
                h['name'] = 'twopair'
                h['rank'] = sorted(q['pair'])[0:1]
            #pair
            elif len(q['pair']) == 1:
                h['name'] = 'pair'
                h['rank'] = q['pair'][0]
        elif q['pocket pair']:
            h['name'] = 'pair'
            h['rank'] = cardA.r
            
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
        
        #booleans if pocket pair or pocket suited. Ranks and suits can be retrieved
        #from pocket[0].r and pocket[0].s
        q['pocket pair'] = (self.pocket[0].r == self.pocket[1].r)
        q['pocket suited'] = (self.pocket[0].s == self.pocket[1].s)
        
        if len(self.board) > 0:
            #dictonary of lists of numerical value of multijple 0 to 12. [] for dne
            q['pair'] = self.get_pairs()        
            q['set'] = self.get_sets()
            q['quad'] = self.get_quads()
            q['straight']  = self.get_straights()
            q['flush'] = self.get_flushes()    
            #The above are all that is required to determine hand rank.
            #For example, a pair and a set make a full house
                
        return q
    
    def hand_draws(self):
        q = {}
        #flush draw
        #if hand has 4 of same suit
        
        #straight draw
        #if hand has four out of:
        #[A0123,01234,12345,23456,...,89TJQ,TJQKA]
        
        #pairs and sets
        return q
    
            
    #returns a list of floats from 0-1 - features that the Hand can see:    
    #DONE:
    #suited (0 or 1) for (F or T)
    #paired (0 or 1) for (F or T)
    #top_card_rank (0-1) for (2-A)
    #bot_card_rank (0-1) for (2-A)
    #rank_diff (0-1) for (
    #TODO:
    #number of outs,draws,etc
    #    
    def get_features(self):
        q = self.made_hand_components()
        
        #Float from 0-1. 1 for A, 0 for 2
        bot_card_rank = q['ranks'][0]/12.0
        top_card_rank = q['ranks'][1]/12.0
        
        #1-(integer difference between the ranks of the cards)/12
        #so that 0.9-1 is connectors and pairs while 0 is far cards
        rank_diff = q['ranks'][1] - q['ranks'][0]
        rank_diff = (rank_diff % 12)/11
        rank_diff = 1 - rank_diff
                
        pairs = 1*q['pocket pair']
        suited = 1*q['pocket suited']
        
        if len(self.board) > 0: #past preflop
            h = self.best_made_hand()
            
            #count outs
            #determine draws
            pass
            
        return [top_card_rank,bot_card_rank,rank_diff,pairs,suited]
    
    #pairs are a combination of:
    #pocket pair
    #semi-pocket pair
    #board pair
    def get_pairs(self):
        #Entries in p are (r,k) where r is the rank and k is the number of hole cards used
        p = []
      
        #Pocket pair
        if self.ranks[0] == self.ranks[1]:
            p.append(self.ranks[0])
      
        #Semipocket pair - half board, half pocket
        for cardA in self.pocket:
            for cardB in self.board:
                if cardA.r == cardB.r:
                    p.append(cardA.r)                        
                
        #Board pair
        for i,cardA in enumerate(self.board):
            for cardB in self.board[i+1:]:
                if cardA.r == cardB.r:
                    p.append(cardA.r)
                    
        return list(set(p))
    
    def get_sets(self):
        s = []
        #2 hole cards
        if self.ranks[0] == self.ranks[1]:
            for card in self.board:
                if card.r == self.ranks[0]:
                    s.append(card.r)
        
        #1 hole card
        for cardA in self.pocket:
            for i,cardB in enumerate(self.board):
                if cardA.r == cardB.r:
                    for cardC in self.board[i+1:]:
                        if cardA.r == cardC.r:
                            s.append(cardA.r)
        
        #0 hole cards
        for i,cardA in enumerate(self.board):
            for j,cardB in enumerate(self.board[i+1:]):
                if cardA.r == cardB.r:
                    for cardC in self.board[j+1:]:
                        if cardA.r == cardC.r:
                            s.append(cardA.r)
        return list(set(s))
    
    #TODO
    def get_quads(self):
        q = []
        
        #2 hole cards
        if self.ranks[0] == self.ranks[1]:
            for i,cardA in enumerate(self.board):
                if cardA.r == self.ranks[0]:
                   for j,cardB in enumerate(self.board[i+1:]):
                       if cardB.r == cardA.r:
                           q.append(cardA.r)
        #1 hole card
        else: 
            for cardA in self.pocket:
                for i,cardB in enumerate(self.board):
                    if cardA.r == cardB.r:
                        for j,cardC in enumerate(self.board[i+1:]):
                            if cardA.r == cardC.r:
                                for cardD in self.board[i+1:]:
                                    if cardA.r == cardD.r:
                                        q.append(cardA.r)
    
        #0 hole cards
        for i,cardA in enumerate(self.board):
            for j,cardB in enumerate(self.board[i+1:]):
                if cardA.r == cardB.r:
                    for k,cardC in enumerate(self.board[j+1:]):
                        if cardA.r == cardC.r:
                            for cardD in self.board[k+1:]:
                                q.append(cardA.r)
        return list(set(q))
    
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
                s.append((start+i-1,hole_cards))                    
        return s        
        
    #get full flushes
    def get_flushes(self):
        f = []
        for suit in range(4):
            hole_cards = 0
            if self.suits.count(suit) == 5:
                flush_cards = tuple(sorted(self.ranks)[:-6:-1])
                for i in self.pocket:
                    if i.s == suit and i.r in flush_cards:
                        hole_cards = hole_cards + 1
                f.append((flush_cards,hole_cards))
        return f

        
    __repr__ = __str__

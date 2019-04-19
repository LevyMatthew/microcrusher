#Single card with suit and rank
class Card(object):    
    #2 is lowest, A is highest
    R = '23456789TJQKA'
    #spade, club, heart, diamond
    S = 'SCHD'    
    
    def __init__(self,card_str):
        self.card_str = card_str.upper()
        if self.card_str[0] in Card.S:
            self.card_str = self.card_str[::-1]
            
        #N = value of cards. 0 for 2, 12 for A
        self.r = Card.to_rank(self.card_str[0])
            
        #S = suit. S0,C1,H2,D3               
        self.s = Card.to_suit(self.card_str[1])        
            
    
    def __str__(self):
        return self.card_str
            
    
    def to_rank(r_str):
        return Card.R.index(r_str)
            
    def to_suit(s_str):
        return Card.S.index(s_str)

    __repr__ = __str__

from card import Card

class Street(object):
    
    all_names = ['HOLE','FLOP','TURN','RIVER']
    
    
    def __init__(self, lines):
        #HOLE FLOP TURN RIVER
        self.name = ' '.join(lines[0].split(' ')[1:2])
        #0 for Hole, 1 for Flop, etc...
        self.stage = Street.all_names.index(self.name)        
        self.actions = lines[1:]     
        self.player_at = {}   
        
    def __str__(self):
        return self.name
        
    def process_actions(self):
        if self.stage == 0: #HOLE
        
            dealt_cards = []
            for action in self.actions:
                if 'Card dealt' in action:
                    cards = [Card(i) for i in action[-8:-3].split(' ')]
                    pos = action.split(' : ')[0][0:]
                    self.player_at[pos] = {}
                    self.player_at[pos]['Cards'] = cards
                    
    __repr__ = __str__
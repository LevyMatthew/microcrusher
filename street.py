class Street(object):
    
    names = ['HOLE','FLOP','TURN','RIVER']
    
    def __init__(self, lines):
        #HOLE FLOP TURN RIVER
        self.name = ' '.join(lines[0].split(' ')[1:2])
        #0 for Hole, 1 for Flop, etc...
        self.stage = Street.names.index(self.name)        
        self.actions = lines[1:]        
        
    def __str__(self):
        return self.name
    
    __repr__ = __str__
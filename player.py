class Player(object):
    
    def __init__(self, seat, position, stack):
        self.seat = seat
        self.position = position
        self.stack = stack
        self.actions = []

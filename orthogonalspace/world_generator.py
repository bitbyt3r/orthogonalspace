class WorldGenerator:
    def __init__(self, parameters):
        self.parameters = parameters

    def player_ship_position(self):
        if 'player_ship_start' in self.parameters:
            return self.parameters['player_ship_start']
        else:
            return (0.0, 0.0, 0.0)

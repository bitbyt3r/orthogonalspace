import ode

universes = []


class Universe:
    def __init__(self, name="Universe", world_generator=None):
        self.name = name
        self.world_generator = world_generator
        self.world = ode.World()
        self.space = ode.SimpleSpace()
        self.entities = []

    def add_entity(self, entity):
        self.entities.append(entity)

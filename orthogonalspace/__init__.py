import ode

universes = {}


class UniverseNotFound(Exception):
    pass


def find_universe(id):
    universe = universes.get(id, None)

    if not universe:
        raise UniverseNotFound()

    return universe


class Universe:
    def __init__(self, id, name="Universe", world_generator=None):
        self.id = id
        self.name = name
        self.world_generator = world_generator
        self.world = ode.World()
        self.space = ode.SimpleSpace()
        self.entities = []
        self.ships = {}
        self.factions = {}

    def add_ship(self, ship):
        self.ships[ship.id] = ship

    def add_entity(self, entity):
        self.entities.append(entity)

    def add_faction(self, faction):
        self.factions[faction.id] = faction

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
        }

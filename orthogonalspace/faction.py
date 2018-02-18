factions = {}


class Faction:
    def __init__(self, id, name, universe):
        self.id = id
        self.name = name
        self.universe = universe

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "universe_id": self.universe.id,
        }

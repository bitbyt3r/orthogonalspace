from orthogonalspace.entities.entity import Entity


class Ship(Entity):
    def __init__(self, *args, name=None, configuration=None, faction=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.launched = False
        self.name = name or "Spacey McSpaceface"
        self.configuration = configuration or {}
        self.faction = faction

    def launch(self):
        self.universe.add_entity(self)
        self.launched = True

    def to_json(self):
        res = super().to_json()
        res.update({
            "launched": self.launched,
            "name": self.name,
            "configuration": self.configuration,
            "faction_id": self.faction.id,
        })

        return res

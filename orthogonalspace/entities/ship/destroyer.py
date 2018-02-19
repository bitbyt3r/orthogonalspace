from orthogonalspace.entities.ship import Ship


class Destroyer(Ship):
    METADATA = {
        "name": "Destroyer",
        "description": "Destroys things, hopefully",
        "geometry": "cone",
    }

    @classmethod
    def component_slots(cls):
        return [
            "engine.standard",
            "engine.standard",
            "engine.special",
            "weapon.beam",
            "weapon.tube",
            "weapon.tube",
            "weapon.tube",
            "bay",
            "bay",
            "scanner",
            "shield",
            "antenna",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

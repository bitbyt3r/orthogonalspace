from orthogonalspace.entities.ship import Ship


class Destroyer(Ship):
    METADATA = {
        "name": "Carrier",
        "description": "Has lots of fighter bays and not much else",
        "geometry": "box",
    }

    @classmethod
    def component_slots(cls):
        return [
            "engine.standard",
            "engine.special",
            "weapon.beam",
            "bay",
            "bay",
            "bay",
            "bay",
            "bay",
            "bay",
            "scanner",
            "shield",
            "antenna",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

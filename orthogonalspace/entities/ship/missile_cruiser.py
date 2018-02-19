from orthogonalspace.entities.ship import Ship


class MissileCruiser(Ship):
    METADATA = {
        "name": "Missile Cruiser",
        "description": "Has a whole bunch of missile tubes",
        "geometry": "cylinder",
    }

    @classmethod
    def component_slots(cls):
        return [
            "engine.standard",
            "engine.standard",
            "engine.standard",
            "engine.special",
            "weapon.beam",
            "weapon.tube",
            "weapon.tube",
            "weapon.tube",
            "weapon.tube",
            "weapon.tube",
            "weapon.tube",
            "weapon.tube",
            "weapon.tube",
            "scanner",
            "shield",
            "antenna",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

from orthogonalspace.entities.ship import Ship


class Destroyer(Ship):
    DESCRIPTION = "Destroyer"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def component_slots(self):
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

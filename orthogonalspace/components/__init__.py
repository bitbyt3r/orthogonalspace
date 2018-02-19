
SLOT_NAMES = {
    "engine": "Propulsion",
    "engine.standard": "Standard Engine",
    "engine.standard.impulse": "Impulse Drive",
    "engine.special": "Special Drive",
    "engine.special.warp": "Warp Drive",
    "engine.special.jump": "Jump Drive",
    "weapon": "Weapons System",
    "weapon.beam": "Energy Weapon",
    "weapon.beam.small": "Small Energy Weapon",
    "weapon.beam.large": "Large Energy Weapon",
    "weapon.tube": "Torpedo Tube",
    "weapon.tube.small": "Small Torpedo Tube",
    "weapon.tube.large": "Large Torpedo Tube",
    "bay": "Docking Bay",
    "bay.small": "Small Berthing Bay",
    "bay.large": "Large Berthing Bay",
    "scanner": "Scanning System",
    "shield": "Shield Generator",
    "shield.front": "Front Shield Generator",
    "shield.rear": "Rear Shield Generator",
    "shield.port": "Port Shield Generator",
    "shield.starboard": "Starboard Shield Generator",
    "antenna": "Communications Antenna",
}


def describe_slot(name):
    return SLOT_NAMES.get(name, name)


class Component:
    def __init__(self):
        pass

    def slot_type(self):
        return ""

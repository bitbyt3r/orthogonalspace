from orthogonalspace.entities.entity import Entity

import txaio

log = txaio.make_logger()


class Ship(Entity):
    REGISTRY = {}

    METADATA = {
        "name": "",
        "description": "",
        "geometry": "sphere",
    }

    @classmethod
    def type_info(cls):
        return {k: getattr(s, "METADATA", {}) for k, s in cls.REGISTRY.items()}

    @classmethod
    def type_name(cls):
        return getattr(cls, "METADATA", {}).get("name", cls.__name__)

    @classmethod
    def component_slots(cls):
        return []

    def __init__(self, *args, name=None, configuration=None, faction=None, **kwargs):
        super().__init__(*args, geometry=self.type_info().get("geometry", "sphere"), **kwargs)
        self.launched = False
        self.name = name or "Spacey McSpaceface"
        self.configuration = configuration or {}
        self.faction = faction

    def launch(self):
        self.universe.add_ship(self)
        self.universe.add_entity(self)
        self.launched = True

    async def tick(self, dt):
        log.debug("Ship Position: {pos}", pos=str(self.position))

    @property
    def type(self):
        return type(self).type_name()

    def validate_components(self):
        filled_slots = []
        remaining_slots = sorted(self.component_slots(), key=lambda s: (-s.count("."), s))

        for component in self.configuration.get("components", []):
            for i, slot in enumerate(remaining_slots):
                if slot.startswith(component.slot_type()):
                    filled_slots.append(remaining_slots.pop(i))
                    break
            else:
                log.info("Component %s does not fit in this ship", component)
                return False

        log.info("Components validated with %d empty slots", len(remaining_slots))
        return True

    def to_json(self):
        res = super().to_json()
        res.update({
            "launched": self.launched,
            "name": self.name,
            "configuration": self.configuration,
            "faction_id": self.faction.id,
            "type": self.type,
            "slots": self.component_slots(),
        })

        return res

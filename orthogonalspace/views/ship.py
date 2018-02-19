from orthogonalspace.universe import universes, UniverseNotFound, find_universe, Universe
from orthogonalspace.faction import factions
from orthogonalspace.entities.ship import Ship
from orthogonalspace.entities import all_entities
from orthogonalspace.views import register

import uuid
import txaio

log = txaio.make_logger()


class ShipConfig:
    CONFIGS = {}

    def __init__(self, id, universe, name=None, configuration=None, faction=None):
        self.__type = None
        self.launched = False
        self.name = name or "Spacey McSpaceface"
        self.configuration = configuration or {}
        self.faction = faction

        self.CONFIGS[id] = self

    def type_class(self):
        return Ship.REGISTRY[self.type] if self.type else Ship

    @property
    def metadata(self):
        return getattr(self.type_class(), "METADATA", {})

    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        if value is not None and value not in Ship.REGISTRY:
            raise ValueError("Invalid ship type")

        self.__type = value

    def launch(self):
        # TODO implement creating ship from this config
        log.warn("Not yet implemented")
        #self.universe.add_entity(self)
        self.launched = True

    def slots(self):
        if self.type:
            return self.type_class().component_slots()

    def validate_components(self):
        filled_slots = []
        remaining_slots = sorted(self.slots(), key=lambda s: (-s.count("."), s))

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
        return {
            "launched": self.launched,
            "name": self.name,
            "configuration": self.configuration,
            "faction_id": self.faction.id,
            "type": self.type,
            "slots": self.slots(),
            "type_metadata": self.metadata,
        }


class ShipNotFound(Exception):
    pass


@register('ship.list_types')
async def ship_list_types(engine):
    return {"success": True, "reason": "", "types": Ship.type_info()}


@register('ship.set_name')
async def ship_set_name(engine, ship_id, name):
    try:
        ship = ShipConfig.CONFIGS.get(ship_id, None)
        if not ship:
            raise ShipNotFound()

        ship.name = name

        return {"success": True, "reason": ""}

    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe"}
    except ShipNotFound:
        return {"success": False, "reason": "Unknown ship"}


@register('ship.set_type')
async def ship_set_name(engine, ship_id, type):
    try:
        ship = ShipConfig.CONFIGS.get(ship_id, None)
        if not ship:
            raise ShipNotFound()

        ship.type = type

        return {"success": True, "reason": ""}

    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe"}
    except ShipNotFound:
        return {"success": False, "reason": "Unknown ship"}


@register('ship.create')
async def ship_create(engine, faction_id, name=None):
    try:
        faction = factions.get(faction_id, None)

        if not faction:
            return {"success": False, "reason": "Faction not found"}

        universe = faction.universe
        ship = ShipConfig(str(uuid.uuid4()), universe, name=name, faction=faction)

        return {"success": True, "reason": "", "ship": ship}
    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe"}


@register('ship.launch')
async def ship_launch(engine, ship_id):
    try:
        ship = ShipConfig.CONFIGS.get(ship_id, None)
        if not ship:
            raise ShipNotFound()

        ship.launch()

        return {"success": True, "reason": ""}

    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe"}
    except ShipNotFound:
        return {"success": False, "reason": "Unknown ship"}


@register('ship.update_configuration')
async def ship_launch(engine, ship_id, configuration=None):
    try:
        ship = ShipConfig.CONFIGS.get(ship_id, None)
        if not ship:
            raise ShipNotFound()

        ship.configuration.update(configuration or {})

        return {"success": True, "reason": ""}

    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe"}
    except ShipNotFound:
        return {"success": False, "reason": "Unknown ship"}


@register('ship.get')
async def ship_get(engine, ship_id):
    try:
        ship = ShipConfig.CONFIGS.get(ship_id, None)
        if not ship:
            raise ShipNotFound()

        return {"success": True, "reason": "", "ship": ship}

    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe"}
    except ShipNotFound:
        return {"success": False, "reason": "Unknown ship"}

from orthogonalspace.universe import universes, UniverseNotFound, find_universe, Universe
from orthogonalspace.faction import factions
from orthogonalspace.entities.ship import Ship
from orthogonalspace.entities import all_entities
from orthogonalspace.views import register

import uuid
import txaio

log = txaio.make_logger()


class ShipNotFound(Exception):
    pass


@register('ship.list_types')
async def ship_list_types(engine):
    return {"success": True, "reason": "", "types": Ship.type_map()}


@register('ship.create')
async def ship_create(engine, faction_id, name=None):
    try:
        faction = factions.get(faction_id, None)

        if not faction:
            return {"success": False, "reason": "Faction not found"}

        universe = faction.universe
        ship = Ship(str(uuid.uuid4()), universe, name=name, faction=faction)
        all_entities[ship.id] = ship
        universe.add_ship(ship)

        return {"success": True, "reason": "", "ship": ship}
    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe"}


@register('ship.launch')
async def ship_launch(engine, ship_id):
    try:
        ship = all_entities.get(ship_id, None)
        if not ship:
            raise ShipNotFound()

        ship.launch()

        return {"success": True, "reason": ""}

    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe"}
    except ShipNotFound:
        return {"success": False, "reason": "Unknown ship"}


@register('ship.update_parameters')
async def ship_launch(engine, ship_id, parameters=None):
    try:
        ship = all_entities.get(ship_id, None)
        if not ship:
            raise ShipNotFound()

        ship.parameters.update(parameters or {})

        return {"success": True, "reason": ""}

    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe"}
    except ShipNotFound:
        return {"success": False, "reason": "Unknown ship"}


@register('ship.get')
async def ship_get(engine, ship_id):
    try:
        ship = all_entities.get(ship_id, None)
        if not ship:
            raise ShipNotFound()

        return {"success": True, "reason": "", "ship": ship}

    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe"}
    except ShipNotFound:
        return {"success": False, "reason": "Unknown ship"}

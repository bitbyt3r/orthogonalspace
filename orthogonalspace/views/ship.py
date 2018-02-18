from orthogonalspace import Universe, universes, find_universe, UniverseNotFound
from orthogonalspace.entities.ship import Ship
from orthogonalspace.views import register

import uuid
import txaio

log = txaio.make_logger()


class ShipNotFound(Exception):
    pass


@register('ship.create')
async def ship_create(engine, universe_id, faction_id, name=None):
    try:
        universe = find_universe(universe_id)

        ship = Ship(str(uuid.uuid4()), universe, name=name, faction=faction_id)

        universe.add_ship(ship)

        return {"success": True, "reason": "", "ship": ship}
    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe"}


@register('ship.launch')
async def ship_launch(engine, universe_id, ship_id):
    try:
        universe = find_universe(universe_id)

        ship = universe.ships.get(ship_id, None)
        if not ship:
            raise ShipNotFound()

        ship.launch()

        return {"success": True, "reason": ""}

    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe"}
    except ShipNotFound:
        return {"success": False, "reason": "Unknown ship"}


@register('ship.update_parameters')
async def ship_launch(engine, universe_id, ship_id, parameters=None):
    try:
        universe = find_universe(universe_id)

        ship = universe.ships.get(ship_id, None)
        if not ship:
            raise ShipNotFound()

        ship.parameters.update(parameters or {})

        return {"success": True, "reason": ""}

    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe"}
    except ShipNotFound:
        return {"success": False, "reason": "Unknown ship"}


@register('ship.get')
async def ship_get(engine, universe_id, ship_id):
    try:
        universe = find_universe(universe_id)

        ship = universe.ships.get(ship_id, None)
        if not ship:
            raise ShipNotFound()

        return {"success": True, "reason": "", "ship": ship}

    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe"}
    except ShipNotFound:
        return {"success": False, "reason": "Unknown ship"}

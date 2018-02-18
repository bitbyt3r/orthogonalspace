from orthogonalspace.universe import universes, UniverseNotFound, find_universe, Universe
from orthogonalspace.faction import Faction
from orthogonalspace.world_generator import WorldGenerator
from orthogonalspace.views import register

import uuid
import txaio

log = txaio.make_logger()


@register('faction.create')
async def faction_create(engine, universe_id, name):
    try:
        universe = find_universe(universe_id)
        new_faction = Faction(id=str(uuid.uuid4()), name=name, universe=universe)
        universe.add_faction(new_faction)

        return {"success": True, "reason": "", "faction": new_faction}
    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe ID"}


@register('faction.get')
async def universe_get(engine, universe_id, faction_id):
    try:
        universe = find_universe(universe_id)
        faction = universe.factions.get(faction_id, None)

        if not faction:
            return {"success": False, "reason": "Unknown faction ID"}

        return {"success": True, "faction": faction, "reason": ""}
    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe ID"}


@register('faction.set_name')
async def faction_set_name(engine, universe_id, faction_id, name):
    try:
        universe = find_universe(universe_id)
        faction = universe.factions.get(faction_id, None)

        if not faction:
            return {"success": False, "reason": "Unknown faction ID"}

        faction.name = name

        return {"success": True, "faction": faction, "reason": ""}
    except UniverseNotFound:
        return {"success": False, "reason": "Unknown universe ID"}

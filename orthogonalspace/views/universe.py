from orthogonalspace import Universe, universes
from orthogonalspace.world_generator import WorldGenerator
from orthogonalspace.views import register

import uuid
import txaio

log = txaio.make_logger()


@register('universe.create')
async def universe_create(engine, name=None, parameters=None):
    new_universe = Universe(str(uuid.uuid4()), name, world_generator=WorldGenerator(parameters or {}))

    universes[new_universe.id] = new_universe

    return {"success": True, "id": new_universe.id, "name": new_universe.name, "reason": ""}


@register('universe.list')
async def universe_list(engine):
    return universes


@register('universe.get')
async def universe_get(engine, id):
    if id in universes:
        return {"success": True, "universe": universes[id], "reason": ""}
    else:
        return {"success": False,"reason": "Unknown universe ID"}
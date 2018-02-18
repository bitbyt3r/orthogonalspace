from orthogonalspace import Universe, universes
from orthogonalspace.world_generator import WorldGenerator
from orthogonalspace.views import register

import txaio

log = txaio.make_logger()


@register('universe.create')
async def universe_create(engine, name=None, parameters=Nnoe):
    new_universe = Universe(name, world_generator=WorldGenerator(parameters or {}))

    universes.append(new_universe)

    return len(universes)-1


@register('universe.list')
async def universe_list(engine):
    return [{"name": universe.name} for universe in universes]

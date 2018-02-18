from orthogonalspace import Universe, universes
from orthogonalspace.world_generator import WorldGenerator
from orthogonalspace.views import register

import txaio

log = txaio.make_logger()


@register('universe.create')
async def universe_create(name, parameters):
    new_universe = Universe(name, world_generator=WorldGenerator(parameters))

    universes.append(new_universe)

    return len(universes)-1


@register('universe.list')
async def universe_list():
    return [{"name": universe.name} for universe in universes]

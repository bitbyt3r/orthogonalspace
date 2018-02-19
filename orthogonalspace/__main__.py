#!/usr/bin/env python3
"""{0}
Orthogonal Space Backend Server

Usage:
  {0}
  {0} --help
  {0} --version
  {0} [--config=<file>] [-v | -vv | -vvv | -vvvv | -q]

Options:
  -h --help           Show this text.
     --version        Print the version.
  -v --verbose        Set verbosity.
  -q --quiet          Suppress output.
  -c --config=<file>  Path to config file[default: /etc/orthogonalspace/conf.json]

"""

from autobahn.asyncio.component import Component, run
from autobahn.wamp.types import RegisterOptions
from autobahn.wamp import serializer

import importlib
import pkgutil
import asyncio
import signal
import concurrent
import functools
import txaio
import sys
import docopt
import ode

import orthogonalspace.database
import orthogonalspace.models
import orthogonalspace.universe
import orthogonalspace.views
import orthogonalspace.configure
from orthogonalspace.configure import config
import orthogonalspace.serializer
from orthogonalspace.entities.ship import Ship

GAME_SPEED = 1.0
TICK_RATE = 30
STEP_SIZE = 1 / TICK_RATE * GAME_SPEED

log = txaio.make_logger()
txaio.start_logging()
running = True

serializer.JsonObjectSerializer.serialize = orthogonalspace.serializer.serialize
serializer.JsonObjectSerializer.unserialize = orthogonalspace.serializer.unserialize


def collide_callback(args, obj1: ode.GeomObject, obj2: ode.GeomObject):
    if ode.areConnected(obj1.getBody(), obj2.getBody()):
        pass

    print("COLLISION!!!!")

    contacts = ode.collide(obj1, obj2)

    world, joint_group = args

    for c in contacts:
        j = ode.ContactJoint(world, joint_group, c)
        j.attach(obj1.getBody(), obj2.getBody())


async def step(universes, joint_group):
    for universe in universes.values():
        universe.space.collide((universe.world, joint_group), collide_callback)
        universe.world.step(STEP_SIZE)

        for entity in universe.entities:
            await entity.tick(STEP_SIZE)

        joint_group.empty()


def all_subclasses(cls):
    for subclass in cls.__subclasses__():
        yield from all_subclasses(subclass)
        yield subclass


def import_submodules(package, recursive=True):
    """ Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        results[full_name] = importlib.import_module(full_name)
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


async def load_ship_types():
    # Recursively load everything from utils so that we get all the block and resource types registered
    SHIPS = 'orthogonalspace.entities.ship'
    import_submodules(SHIPS)

    # Add all the resources to the registry
    for sub in all_subclasses(Ship):
        name = sub.__name__
        key = '.'.join((sub.__module__, name))

        if key.startswith(SHIPS):
            key = key[len(SHIPS):]

        log.debug("Loaded ship %s", key)
        Ship.REGISTRY[key] = sub


async def game_loop(loop, universes):
    while running:
        joint_group = ode.JointGroup()

        start = loop.time()
        await step(universes, joint_group)
        await asyncio.sleep(max(0, 1 / TICK_RATE - (loop.time() - start)))


def main():
    @asyncio.coroutine
    def exit():
        return loop.stop()

    def nicely_exit(signal):
        log.info("Shutting down due to {signal}", signal=signal)
        global running
        running = False
        for task in asyncio.Task.all_tasks():
            task.cancel()
        asyncio.ensure_future(exit())

    # Kill the loop on Ctrl+C
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, functools.partial(nicely_exit, 'SIGINT'))
    loop.add_signal_handler(signal.SIGTERM, functools.partial(nicely_exit, 'SIGTERM'))

    arguments = docopt.docopt(__doc__.format(sys.argv[0]), version="2.0.0")
    arguments = {k.lstrip('--'): v for k, v in arguments.items()}

    verbose = arguments.get("verbose", 0)
    quiet = arguments.get("quiet", 0)
    level = "error"
    if verbose == 1:
        level = "warn"
    elif verbose == 2:
        level = "info"
    elif verbose == 3:
        level = "debug"
    elif verbose == 4:
        level = "trace"
    elif quiet == 1:
        level = "critical"
    txaio.start_logging(level)

    orthogonalspace.configure.get_config(arguments.get("config", "/etc/orthogonalspace/conf.json"))

    async def run_database():
        while running:
            try:
                await orthogonalspace.database.initialize(config=config, callback=start)
            except concurrent.futures._base.CancelledError as e:
                if not running:
                    pass
                else:
                    print("Unexpected cancelled future: {}".format(e))
            except RuntimeError as e:
                if not running:
                    pass
                else:
                    # Usually means the connection to the crossbar server was lost.
                    print("Runtime Error: {}".format(e))

    loop.run_until_complete(asyncio.gather(run_database(), game_loop(loop,
                                                                     orthogonalspace.universe.universes)))

    loop.close()

async def start(config=None, engine=None):
    loop = asyncio.get_event_loop()

    # TODO: Read this config from the config object
    component = Component(
        transports=[
            {
                "type": "websocket",
                "url": u"ws://localhost:8083/ws",
                "endpoint": {
                    "type": "tcp",
                    "host": "localhost",
                    "port": 8080,
                },
                "options": {
                    "open_handshake_timeout": 100,
                },
                "serializers": [
                    "json"
                ]
            },
        ],
        realm=u"realm1",
        extra=engine,
    )

    @component.on_join
    def join(session, details):
        log.debug("Joined crossbar server")
        log.debug("Registering methods")
        for function in orthogonalspace.views.registrations:
            log.debug("  Registering {}".format(function['name']))
            session.register(functools.partial(function['method'], engine), function['name'], options = RegisterOptions(**function['options']))

    @component.on_disconnect
    def disconnect(session, was_clean):
        # This connection has died, so kill the loop and let a new one get created
        loop.stop()

    await component.start(loop)

if __name__ == "__main__":
    main()

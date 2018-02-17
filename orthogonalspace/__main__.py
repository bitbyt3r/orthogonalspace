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

import asyncio
import signal
import concurrent
import functools
import txaio
import sys
import docopt

import orthogonalspace.database
import orthogonalspace.models
import orthogonalspace.views
import orthogonalspace.configure
from orthogonalspace.configure import config
import orthogonalspace.serializer

log = txaio.make_logger()
txaio.start_logging()
running = True

serializer.JsonObjectSerializer.serialize = orthogonalspace.serializer.serialize
serializer.JsonObjectSerializer.unserialize = orthogonalspace.serializer.unserialize


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

    while running:
        try:
            task = orthogonalspace.database.initialize(config=config, callback=start)
            loop.run_until_complete(task)
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

import os
import asyncio
from yoyo import read_migrations, get_backend
from pprint import pprint
import txaio
log = txaio.make_logger()

async def initialize(config=None, callback=None):
    # TODO: Read this config from the config object
    if config['db_engine'] == "postgres":
        import aiopg.sa
        async with aiopg.sa.create_engine(user=config['db_user'],
                                 database=config['db_database'],
                                 host=config['db_host'],
                                 password=config['db_pass']) as engine:

            ## Run Migrations
            log.info("Running Migrations")
            backend = get_backend('postgres://{}:{}@{}/{}'.format(config['db_user'], config['db_pass'], config['db_host'], config['db_database']))
            if os.path.isdir(config.get('db_migrations', "")):
                migrations = read_migrations(config.get('db_migrations', ""))
            else:
                migrations = read_migrations('/usr/lib/orthogonalspace/migrations')
            backend.apply_migrations(backend.to_apply(migrations))

            if callback:
                await callback(engine=engine, config=config)
    elif config['db_engine'] == "sqlite":
        import aiosqlite
        async with aiosqlite.connect(config['db_path']) as engine:

            class acquire_wrapper:
                def __init__(self):
                    pass
                async def __aenter__(self):
                    class conn_handler:
                        def __init__(self, engine):
                            self.engine = engine
                        def execute(self, statement):
                            return self.engine.execute(str(statement), statement.compile().params)

                    return conn_handler(engine)
                async def __aexit__(self, *args):
                    pass
            engine.acquire = acquire_wrapper

            ## Run Migrations
            log.info("Running Migrations")
            backend = get_backend('sqlite:///{}'.format(config['db_path']))
            if os.path.isdir(config.get('db_migrations', "")):
                migrations = read_migrations(config.get('db_migrations', ""))
            else:
                migrations = read_migrations('/usr/lib/orthogonalspace/migrations')
            backend.apply_migrations(backend.to_apply(migrations))

            if callback:
                await callback(engine=engine, config=config)
    else:
        log.error("Unknown database engine {}".format(config['db_engine']))


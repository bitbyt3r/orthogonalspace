import os
import sys
import json
import txaio

log = txaio.make_logger()

config = {
            "db_user": "orthogonalspace",
            "db_pass": "password",
            "db_host": "localhost",
            "db_database": "orthogonalspace",
        }

def get_config(path=""):
    if not path:
        path = "/etc/orthogonalspace/conf.json"
        if not os.path.isfile(path):
            log.info("No config file provided. Continuing with defaults.")
            return
    elif not path:
        sys.exit("{} is not a file. Could not load config.".format(path))
    try:
        newconfig = json.load(path)
    except:
        sys.exit("Could not parse config file: {}".format(path))
    config.update(newconfig)
    return

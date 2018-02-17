#!/usr/bin/python
import orthogonalspace.models
import datetime

filename = "{}-001-create_table.py".format(datetime.datetime.now().isoformat())

with open(filename, "w") as MIGRATE_FILE:
    MIGRATE_FILE.write("from yoyo import step\n\n")
    for i in orthogonalspace.models.modules:
        up, down = orthogonalspace.models.create_table(i)
        step = 'step("""{}""", """{}""")\n'.format(up, down)
        print(step)
        MIGRATE_FILE.write(step)

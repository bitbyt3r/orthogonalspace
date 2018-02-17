#!/usr/bin/env python3
import autobahn_sync
import readline
import json
import sys
import re
while True:
  try:
    wamp = autobahn_sync.AutobahnSync()
    wamp.run(url='ws://localhost:8080/ws', realm='realm1')
    query = input(":")
    m = re.search('^([^ ]*)\s*(\[.*\])?\s*(\{.*\})?$', query)
    parts = m.groups()
    args = []
    kwargs = {}
    if parts[0]:
      function = parts[0]
    if parts[1]:
      args = json.loads(parts[1])
    if parts[2]:
      kwargs = json.loads(parts[2])
    print("Calling {}({}{}{})".format(function, ", ".join(map(str, args)), ", " if args and kwargs else "", ", ".join(["{}={}".format(x, json.dumps(kwargs[x])) for x in kwargs.keys()])))
    data = wamp.session.call(function, *args, **kwargs)
    print(json.dumps(data, sort_keys=True, indent=2, separators=(',', ':')))
  except Exception as e:
    print(e)

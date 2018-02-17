import pkgutil
import importlib
import functools
import time

registrations = []

def register(*args, **kwargs):
    if args:
        if callable(args[0]):
            options = {}
            if 'options' in kwargs.keys():
                options = kwargs['options']
            name = ""
            if 'name' in kwargs.keys():
                name = kwargs['name']
            if len(args) > 1:
                name = args[1]
            if not name:
                name = args[0].__name__
            registrations.append({'method': args[0], 'name': name, 'options': options})
            return args[0]
        return functools.partial(register, name=args[0], **kwargs)
    return functools.partial(register, **kwargs)

class timer():
    def __init__(self, msg):
        self.msg = msg
    def __enter__(self):
        self.start = time.time()
    def __exit__(self,exc_type,exc_value,traceback):
        print(self.msg.format(int((time.time() - self.start)*1000)))
        
pkgs = pkgutil.walk_packages(__path__)
for i in pkgs:
    importlib.import_module(__name__ + "." + i.name)

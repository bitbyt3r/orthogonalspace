#!venv/bin/python
from setuptools import setup, find_packages
import subprocess
import os
import sys
from pip.req import parse_requirements

# Setuptools bug workaround issue #10945
import codecs
try:
    codecs.lookup('mbcs')
except LookupError:
    ascii = codecs.lookup('ascii')
    func = lambda name, enc=ascii: {True: enc}.get(name == 'mbcs')
    codecs.register(func)

cmd = "git describe --tags --abbrev=0 HEAD"
result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
git_tag = result.stdout.readlines()[0].strip().decode('ASCII')
version_num = git_tag.lstrip('v')

cmd = "git rev-list {}..HEAD --count".format(git_tag)
result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
release_num = result.stdout.readlines()[0].strip().decode('ASCII')

print("Building {}-{}".format(version_num, release_num))

migrations = []

print(os.environ)
if os.environ.get('RPM_MODE') == "true":
    print("Adding migration files")
    for x in os.walk("migrations"):
        migrations.append((os.path.join('/usr/lib/orthogonalspace/', x[0]), [os.path.join(x[0], y) for y in x[2]]))
else:
    print("Not adding migration files")

setup(
    name='orthogonalspace',
    packages=find_packages(exclude=['etc', 'contrib']),
    version=version_num,
    description='Spacebridge Simulator',
    long_description="""Gather with your friends to play a game in space!""",
    license="GPLv3",
    author='Hackafe',
    author_email='mark@hackafe.net',
    url='git@github.com:bitbyt3r/orthogonalspace.git',
    keywords=[
        '3d', 'game',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: No Input/Output (Daemon)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
    ],
    install_requires=[
        'autobahn',
        'pyasn1',
        'aiopg',
        'yoyo-migrations',
        'autobahn_sync',
    ],
    data_files=migrations,
    entry_points={
        'console_scripts': [
            'orthogonalspace=orthogonalspace.__main__:main',
        ]
    },
)

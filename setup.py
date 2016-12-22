import os
from setuptools import setup

setup(
    name='up',
    version='0.5',
    packages=['up', 'up.utils', 'up.commands', 'up.providers', 'up.flight_controller'],
    url='',
    license='',
    author='Michal Raska',
    author_email='michal.raska@gmail.com',
    description='',
    install_requires=['twisted', 'colorlog', 'psutil', 'pyyaml'],
    data_files=[(os.path.expanduser('~') + '/up/config/', ['up/config/config.cfg', 'up/config/modules.cfg'])],
    scripts=['bin/up']
)

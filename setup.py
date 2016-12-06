import os
from distutils.core import setup

setup(
    name='up',
    version='0.5',
    packages=['up', 'up.utils', 'up.commands', 'up.providers', 'up.flight_controller'],
    url='',
    license='',
    author='Michal Raška',
    author_email='michal.raska@gmail.com',
    description='',
    requires=['twisted', 'colorlog', 'psutil', 'pyserial'],
    data_files=[(os.path.expanduser('~') + '/up/config/', ['up/config/config.cfg', 'up/config/modules.cfg'])]
)

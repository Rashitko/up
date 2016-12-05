from distutils.core import setup

setup(
    name='up',
    version='0.5',
    packages=['', 'utils', 'commands', 'providers', 'flight_controller'],
    url='',
    license='MIT',
    author='michal',
    author_email='michal.raska@gmail.com',
    description='Up is the modular framework for creating autopilot systems.',
    requires=['twisted', 'colorlog', 'pyserial', 'psutil']
)

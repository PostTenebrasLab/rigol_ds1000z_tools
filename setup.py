from distutils.core import setup

setup(
    name='rigol_ds1000z_tools',
    version='1.0.1',
    packages=[''],
    url='https://github.com/PostTenebrasLab/rigol_ds1000z_tools',
    license='GPLv3',
    author='Sebastien Chassot (sinux)',
    author_email='sebastien@sinux.net',
    description='Simple script to acquire data from a Rigol DS1000z oscilloscope using Python'
)

install_requires = ['matplotlib']
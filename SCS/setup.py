#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup


setup(name='SCS',
    version='1.0',
    description='SCS bus Library',
    author='Michele',
    author_email='',
    url='https://scsshield.altervista.org/',
    install_requires=['janus', 'asyncserial', 'asyncio_mqtt', 'tinydb', 'gmqtt', 'uvloop'],
    #packages=['janus', 'asyncserial', 'asyncio_mqtt', 'tinydb', 'gmqtt', 'uvloop'],
    python='>=3.6, <4',
    )
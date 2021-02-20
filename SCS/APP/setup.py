#!/usr/bin/env python

from distutils.core import setup

setup(name='SCS',
      version='1.0',
      description='SCS bus Library',
      author='Michele',
      author_email='',
      url='https://scsshield.altervista.org/',
      packages=['janus', 'asyncserial', 'asyncio_mqtt', 'tinydb'],
     )
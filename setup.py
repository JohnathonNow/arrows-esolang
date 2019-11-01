#!/usr/bin/env python3
from setuptools import setup

setup(
    name='arrows_esolang',
    version='1.0.1',
    author='John Westhoff',
    author_email='johnjwesthoff@gmail.com',
    description=('An esoteric language that uses drawings of arrows.'),
    url='https://github.com/JohnathonNow/arrows-esolang',
    packages=['arrows_esolang'],
    test_suite='tests',
    scripts=['bin/arrows', 'bin/arrowsc'],
    install_requires=['pillow', 'enum-compat'],
    include_package_data=True,
)

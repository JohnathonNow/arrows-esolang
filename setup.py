#!/usr/bin/env python3
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='arrows_esolang',
    version='1.0.2',
    author='John Westhoff',
    author_email='johnjwesthoff@gmail.com',
    description=('An esoteric language that uses drawings of arrows.'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/JohnathonNow/arrows-esolang',
    packages=setuptools.find_packages(),
    test_suite='tests',
    scripts=['bin/arrows', 'bin/arrowsc'],
    install_requires=['pillow', 'enum-compat'],
    include_package_data=True,
)

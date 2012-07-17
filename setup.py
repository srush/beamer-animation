#!/usr/bin/env python

from setuptools import setup

setup(name='beamer-animation',
      version='1.0',
      description='Beamer animation.',
      license='BSD',
      author='Alexander Rush',
      author_email='sasha.rush@gmail.com',
      url='http://www.github.com/srush/beamer-animation',
      packages=["beamer_animation"],
      include_package_data=True,
      entry_points = """
      [console_scripts]
      beamer-animation-quickstart=beamer_animation.quickstart:main
      """
      )

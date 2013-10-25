from setuptools import setup

setup(
  name='moretools',
  version='0.1a28',
  description=(
    'Many more basic tools for python 2/3'
    ' extending itertools, functools, operator and collections.'
    ),
  author='Stefan Zimmermann',
  author_email='zimmermann.code@gmail.com',
  url='http://bitbucket.org/userzimmermann/python-moretools',

  license='LGPLv3',

  packages=['moretools'],

  use_2to3=True,
  use_2to3_exclude_fixers=['lib2to3.fixes.fix_' + fix for fix in [
    'dict',
    'map',
    'filter',
    'reduce',
    ]],

  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved ::'
    ' GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development',
    'Topic :: Utilities',
    ],
  keywords=[
    'tools', 'itertools', 'functools', 'operator', 'collections',
    'iterator', 'iteration', 'functional',
    'filter', 'map', 'repeat', 'query',
    'tuple', 'list', 'set', 'dict', 'simpledict',
    'camelize', 'decamelize',
    'python3',
    ],
  )

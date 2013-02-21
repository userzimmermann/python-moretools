from setuptools import setup

setup(
  name = 'python-moretools',
  version = '0.1a8',
  description = (
    'many more basic tools for python 2/3'
    + ' extending itertools, functools operator and collections'
    ),

  author = 'Stefan Zimmermann',
  author_email = 'zimmermann.code@gmail.com',
  url = 'http://bitbucket.org/StefanZimmermann/python-moretools',

  license = 'LGPLv3',

  packages = ['moretools'],

  classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved ::'
    + ' GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Topic :: Software Development',
    'Topic :: Utilities',
    ],

  keywords = [
    'tools', 'itertools', 'functools', 'operator', 'collections',
    'iterator', 'iteration', 'functional',
    'filter', 'map', 'repeat', 'query',
    'tuple', 'list', 'set', 'dict', 'simpledict',
    'python3',
    ],
  )

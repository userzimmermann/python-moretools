from distutils.core import setup

setup(
  name = 'python-moretools',
  version = '0.1a',
  description = (
    'many more basic tools for python 2/3'
    + ' extending itertools, functools and operator'
    ),

  author = 'Stefan Zimmermann',
  author_email = 'zimmermann.code@googlemail.com',
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
    'tools', 'itertools', 'functools', 'operator',
    'iterator', 'iteration', 'functional',
    'filter', 'map', 'repeat', 'query',
    'python3',
    ],
  )

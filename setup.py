try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
  name='moretools',
  version='0.1a33',
  description=(
    'Many more basic tools for python 2/3'
    ' extending itertools, functools, operator and collections.'
    ),
  author='Stefan Zimmermann',
  author_email='zimmermann.code@gmail.com',
  url='http://bitbucket.org/userzimmermann/python-moretools',

  license='LGPLv3',

  install_requires=['six'],

  packages=['moretools'],

  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved ::'
    ' GNU Library or Lesser General Public License (LGPL)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
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

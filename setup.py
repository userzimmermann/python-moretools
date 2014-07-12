import sys
from subprocess import call


exec(open('__init__.py').read())

if 'sdist' in sys.argv:
    status = call('scons')
    if status:
        sys.exit(status)


setup(
  name=NAME,
  version=VERSION,
  description=(
    'Many more basic tools for python 2/3'
    ' extending itertools, functools, operator and collections.'
    ),
  author='Stefan Zimmermann',
  author_email='zimmermann.code@gmail.com',
  url='http://bitbucket.org/userzimmermann/python-moretools',

  license='LGPLv3',

  install_requires=REQUIRES,

  package_dir={
    'moretools.setup': '.',
    },
  packages=[
    'moretools',
    'moretools.setup',
    ],
  package_data={
    'moretools.setup': SETUP_DATA,
    },

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
    'tuple', 'list', 'set', 'dict', 'simpledict', 'frozen', 'struct',
    'dictset', 'dictzip', 'simpledictset', 'simpledictzip',
    'camelize', 'decamelize', 'isidentifier', 'identifier',
    'python3',
    ],
  )

import sys
from subprocess import call


exec(open('__init__.py').read())

if 'sdist' in sys.argv:
    status = call('scons')
    if status:
        sys.exit(status)


zetup(
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
  )

import sys
from subprocess import call


# Run the zetup script:
exec(open('__init__.py').read())


zetup(
  package_dir={
    'moretools.zetup': '.',
    },
  packages=[
    'moretools',
    'moretools.zetup',
    ],
  package_data={
    'moretools.zetup': ZETUP_DATA,
    },
  )

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'six',
    'futures',
    'tornado',
    'urllib3',
    'requests',
    'pytz',
    'PyYAML',
    'argparse'
]

setup(name='tictactoe',
      version='1.0.0',
      description='Tic tac toe api implementation',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='Tic-tac-toe game python tornado api',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points={
          'console_scripts': [
              "tictactoe = tictactoe.app:server",
          ],
      },
  )

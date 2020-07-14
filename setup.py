from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='python-redis-cache',
      version='1.1.1',
      description='Basic Redis caching for functions',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/taylorhakes/python-redis-cache',
      author='Taylor Hakes',
      license='MIT',
      python_requires='>=3.6,<3.9',
      packages=find_packages(),
      setup_requires=['pytest-runner==5.2'],
      tests_require=['pytest==5.4.3', 'redis==3.5.3'],
)

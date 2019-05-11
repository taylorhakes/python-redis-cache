from setuptools import setup, find_packages

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='python-redis-cache',
      version='1.0.0',
      description='Basic Redis caching for functions',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/taylorhakes/python-redis-cache',
      author='Taylor Hakes',
      license='MIT',
      packages=find_packages(),
      setup_requires=['pytest-runner'],
      tests_require=['pytest', 'mock', 'fakeredis'],
)
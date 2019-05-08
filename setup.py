from setuptools import setup, find_packages

setup(name='python-redis-cache',
      version='0.1',
      description='The funniest joke in the world',
      url='http://github.com/storborg/funniest',
      author='Taylor Hakes',
      license='MIT',
      packages=find_packages(),
      setup_requires=['pytest-runner'],
      tests_require=['pytest', 'mock', 'fakeredis'],
)
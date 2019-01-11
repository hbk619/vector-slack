from setuptools import setup, find_packages

setup(name='vectorslack',
      version='0.0.1',
      description='Integrate vector and slack',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      install_requires=[
          'slackclient == 1.3.0',
          'anki_vector == 0.5.1'
      ])

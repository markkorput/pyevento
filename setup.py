from setuptools import setup
import os.path

long_description = ''
with open(os.path.join(os.path.dirname(__name__), 'README.md')) as f:
    long_description = f.read()

setup(name='evento',
      version='1.0.2',
      description='Observer pattern made muy facil',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='http://github.com/markkorput/pyevento',
      author='Mark van de Korput',
      author_email='dr.theman@gmail.com',
      license='MIT',
      packages=['evento'],
      zip_safe=True,
      test_suite='tests')

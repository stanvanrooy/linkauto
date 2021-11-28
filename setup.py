import setuptools
from distutils.core import setup

setup(
  name='linkauto',
  packages=setuptools.find_packages(),
  version='0.0.4',
  license='MIT',
  description='Python wrapper for the private LinkedIn API',
  author='Stan van Rooy',
  author_email='stan@rooy.dev',
  url='https://github.com/stanvanrooy/linkauto',
  download_url='https://github.com/stanvanrooy/linkauto/archive/0.0.1.tar.gz',
  keywords=['linkedin api', 'private linkedin api'],
  install_requires=[
    'orjson',
    'aiohttp'
  ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Libraries :: Python Modules',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
  ],
)

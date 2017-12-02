# noqa: D100
import os
import re
from glob import glob

from setuptools import setup

PKG_VERSION = re.search(
    r'^__version__\s*=\s*[\'"](.+?)[\'"]',
    open(os.path.join(os.path.dirname(__file__),
                      'nbcollate/version.py')).read(), re.M).group(1)

setup(
    name='nbcollate',
    version=PKG_VERSION,
    description='Collate Jupyter Notebooks',
    long_description='Collate Jupyter classroom assignment and submission notebooks',
    url='http://github.com/olin-computing/nbcollate',
    author='Paul Ruvolo, Oliver Steele',
    author_email='steele@osteele.com',
    license='MIT',
    packages=['nbcollate'],
    scripts=glob(os.path.join('scripts', '*')),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
        'Topic :: Education',

    ],
    install_requires=[
        'cached_property',
        'nbconvert',
        'nbformat',
        'numpy',
        'python-Levenshtein',
    ],
)

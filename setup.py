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
    scripts=glob(os.path.join('scripts', '*')),
    description='Collating Jupyter Notebooks',
    long_description='Collate Jupyter assignment notebooks',
    classifiers=[
        'Intended Audience :: Developers', 'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5'
    ],
    url='http://github.com/olin-computing/nbcollate',
    author='Paul Ruvolo, Oliver Steele',
    author_email='steele@osteele.com',
    license='MIT',
    install_requires=[
        'cached_property',
        'nbconvert',
        'nbformat',
        'numpy',
        'python-Levenshtein',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ]
)

# noqa: D100
from setuptools import setup

setup(name='nbcollate',
      version='0.1',
      description='Collating Jupyter Notebooks',
      long_description='Collate Jupyter assignment notebooks',
      classifiers=[
          'Intended Audience :: Developers',
          'Intended Audience :: Education',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3'
          'Programming Language :: Python :: 3.5'
      ],
      url='http://github.com/olin-computing/nbcollate',
      author='Paul Ruvolo, Oliver Steele',
      author_email='steele@osteele.com',
      license='MIT',
      install_requires=[
          'cached_property',
          'nbconvert',
          'numpy',
          'python-Levenshtein',
      ],
      zip_safe=False)

nbcollate
=========

|PyPI version| |Build Status| |Codacy Badge| |Requirements Status| |Updates| |License|

The **nbcollate** package combines a set of Jupyter notebooks into a
single notebook.

It also provides a command-line interface, ``nbcollate``.

Example
-------

::

    nbcollate assignment.ipynb student-*.ipynb

Creates the file |collated|_ from the files in |example-dir|_.

.. |collated| replace:: assignment-collated.ipynb
.. _collated: https://pypi.python.org/pypi/nbcollate
.. |example-dir| replace:: test/files
.. _example-dir: https://github.com/osteele/nbcollate/tree/master/tests/files

Installation
------------

::

    pip install nbcollate

Usage
-----

::

    nbcollate assignment-1.ipynb students/*/assignment-1.ipynb

::

    nbcollate --help

Related Projects
----------------

`classroom-tools <https://github.com/olin-computing/classroom-tools>`__
contains scripts related to using GitHub and Jupyter in education It
includes a command-line interface to an older version of this code. That
script will eventually be modified to use this package.

A web application with similar functionality is at
`olin-computing/assignment-dashboard <https://github.com/olin-computing/assignment-dashboard>`__.
That application caches the state of GitHub in a local database, and
provides a web interface for inspect completion status by student or by
question, and for browsing the original and collated notebooks.

Contributing
------------

Test via any of:

::

    PYTHONPATH=. py.test
    python setup.py test

    docker build -t nbcollate-pytest .
    docker run --rm -it -v `pwd`:/src nbcollate-pytest

Acknowledgements
----------------

This package is inspired by original work
`paulruvolo/SoftDesSp16Prep <https://github.com/paulruvolo/SoftDesSp16Prep>`__
by Paul Ruvolo at Olin College, extended at
`osteele/assignment-tools <https://github.com/osteele/assignment-tools>`__.

.. |PyPI version| image:: https://img.shields.io/pypi/v/nbcollate.svg
   :target: https://pypi.python.org/pypi/nbcollate
   :alt: Latest PyPI Version
.. |Build Status| image:: https://travis-ci.org/osteele/nbcollate.svg?branch=master
   :target: https://travis-ci.org/osteele/nbcollate
   :alt: Build Status
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/f60ffc2534ef45c6acc267dae760b373
   :target: https://www.codacy.com/app/steele/nbcollate?utm_source=github.com&utm_medium=referral&utm_content=osteele/nbcollate&utm_campaign=Badge_Grade
   :alt: Codacy
.. |Requirements Status| image:: https://requires.io/github/osteele/nbcollate/requirements.svg?branch=master
   :target: https://requires.io/github/osteele/nbcollate/requirements/?branch=master
   :alt: Requirements Status
.. |Updates| image:: https://pyup.io/repos/github/osteele/nbcollate/shield.svg
   :target: https://pyup.io/repos/github/osteele/nbcollate/
   :alt: Updates
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/osteele/nbcollate/blob/master/LICENSE
   :alt: License

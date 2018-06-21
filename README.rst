nbcollate
=========

|PyPI version| |Doc Status| |Build Status| |Updates| |License|

This package provides an `API`_, and a command-line interface, to combine a set of
Jupyter notebooks into a single notebook.

The provided functions combine a Jupyter notebook that contains a set of
prompts, and copies of this notebook that answer the prompts, into a single
notebook that lists all the answers after each prompt.

This is intended for use in a classroom setting, to collect assignment
submissions into a notebook that can be quickly reviewed. The notebook can
include student names, or it can be anonymous for use in classroom review. In
the latter case, functionality exists to remove duplicate answers, and to sort
answers by length.

Installation
------------

::

    pip install nbcollate

Command-Line Usage
------------------

::

    nbcollate assignment.ipynb student-*.ipynb

Creates the file |collated|_ from the ``student-*`` files in |example-dir|_.

::

    nbcollate assignment.ipynb student-*.ipynb --label

Same as above, but labels each student with a name derived from the notebook
file name.

.. |collated| replace:: assignment-collated.ipynb
.. _collated: https://github.com/osteele/nbcollate/blob/master/tests/files/assignment-collated.ipynb
.. |example-dir| replace:: test/files
.. _example-dir: https://github.com/osteele/nbcollate/tree/master/tests/files

::

    nbcollate --help

Contributing
------------

Set Up
^^^^^^

Install `pipenv <https://docs.pipenv.org/>`. Then:

::

    pipenv install
    pipenv shell

Test
^^^^

::

    pytest

Release
^^^^^^^

::

    tox
    bumpversion release
    flit publish
    git push --tags

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

Acknowledgements
----------------

This package is inspired by original work
`paulruvolo/SoftDesSp16Prep <https://github.com/paulruvolo/SoftDesSp16Prep>`__
by Paul Ruvolo at Olin College, extended at
`osteele/assignment-tools <https://github.com/osteele/assignment-tools>`__.

License
-------

MIT

.. |PyPI version| image:: https://img.shields.io/pypi/v/nbcollate.svg
    :target: https://pypi.python.org/pypi/nbcollate
    :alt: Latest PyPI Version
.. |Doc Status| image:: https://readthedocs.org/projects/nbcollate/badge/?version=latest
    :target: http://nbcollate.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. |Build Status| image:: https://travis-ci.org/osteele/nbcollate.svg?branch=master
    :target: https://travis-ci.org/osteele/nbcollate
    :alt: Build Status
.. |Updates| image:: https://pyup.io/repos/github/osteele/nbcollate/shield.svg
    :target: https://pyup.io/repos/github/osteele/nbcollate/
    :alt: Updates
.. |License| image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/osteele/nbcollate/blob/master/LICENSE
    :alt: License

.. _API: http://nbcollate.readthedocs.io/en/latest/?badge=latest#module-nbcollate

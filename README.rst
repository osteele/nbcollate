nbcollate
=========

|Build Status| |Codacy Badge| |Requirements Status| |Updates| |image4|

The **nbcollate** package combines a set of Jupyter notebooks into a
single notebook.

It also provides a command-line interface. Execute ``nbcollate --help``
for usage information.

Status
------

This package is in an alpha state. The API may change.

Remaining work includes:

-  [ ] the current algorithm misses response cells
-  [ ] documentation and testing
-  [ ] option to concatenate notebooks
-  [ ] parameterize prompt recognition

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

.. |Build Status| image:: https://travis-ci.org/olin-computing/nbcollate.svg?branch=master
   :target: https://travis-ci.org/olin-computing/nbcollate
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/f60ffc2534ef45c6acc267dae760b373
   :target: https://www.codacy.com/app/steele/nbcollate?utm_source=github.com&utm_medium=referral&utm_content=olin-computing/nbcollate&utm_campaign=Badge_Grade
.. |Requirements Status| image:: https://requires.io/github/olin-computing/nbcollate/requirements.svg?branch=master
   :target: https://requires.io/github/olin-computing/nbcollate/requirements/?branch=master
.. |Updates| image:: https://pyup.io/repos/github/olin-computing/nbcollate/shield.svg
   :target: https://pyup.io/repos/github/olin-computing/nbcollate/
.. |image4| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/osteele/gojekyll/blob/master/LICENSE

# nbcollate

[![Build Status][travis-svg]][travis-url]
[![Codacy Badge][codacy-svg]][codacy-url]
[![Requirements Status][requires-svg]][requires-url]
[![Updates][pyup-svg]][pyup-url]
 [![][license-svg]][license-url]

The **nbcollate** package combines a set of Jupyter notebooks into a single notebook.

It also provides a command-line interface. Execute `nbcollate --help` for usage information.

## Status

This package is in an alpha state. The API may change.

Remaining work includes:

- [ ] the current algorithm misses response cells
- [ ] documentation and testing
- [ ] option to concatenate notebooks
- [ ] parameterize prompt recognition

## Related Projects

[classroom-tools](https://github.com/olin-computing/classroom-tools) contains scripts related to using GitHub and Jupyter in education
It includes a command-line interface to an older version of this code.
That script will eventually be modified to use this package.

A web application with similar functionality is at [olin-computing/assignment-dashboard](https://github.com/olin-computing/assignment-dashboard).
That application caches the state of GitHub in a local database, and provides a web interface for inspect completion status by student or by question,
and for browsing the original and collated notebooks.

## Contributing

Test via any of:

    PYTHONPATH=. py.test
    python setup.py test

    docker build -t nbcollate-pytest .
    docker run --rm -it -v `pwd`:/src nbcollate-pytest

## Acknowledgements

This package is inspired by original work [paulruvolo/SoftDesSp16Prep](https://github.com/paulruvolo/SoftDesSp16Prep)
by Paul Ruvolo at Olin College,
extended at [osteele/assignment-tools](https://github.com/osteele/assignment-tools).

[codacy-svg]: https://api.codacy.com/project/badge/Grade/f60ffc2534ef45c6acc267dae760b373
[codacy-url]: https://www.codacy.com/app/steele/nbcollate?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=olin-computing/nbcollate&amp;utm_campaign=Badge_Grade

[travis-svg]: https://travis-ci.org/olin-computing/nbcollate.svg?branch=master
[travis-url]: https://travis-ci.org/olin-computing/nbcollate

[license-url]: https://github.com/osteele/gojekyll/blob/master/LICENSE
[license-svg]: https://img.shields.io/badge/license-MIT-blue.svg

[pyup-svg]: https://pyup.io/repos/github/olin-computing/nbcollate/shield.svg
[pyup-url]: https://pyup.io/repos/github/olin-computing/nbcollate/

[requires-svg]: https://requires.io/github/olin-computing/nbcollate/requirements.svg?branch=master
[requires-url ]: https://requires.io/github/olin-computing/nbcollate/requirements/?branch=master

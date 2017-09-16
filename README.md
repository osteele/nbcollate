# nbcollate

The **nbcollate** package combines a set of Jupyter notebooks into a single notebook.

## Status

This package is in an alpha state. The API may change.

Remaining work includes:

- [ ] the current algorithm misses response cells
- [ ] documentation and testing
- [ ] add a command-line interface
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

This package is derived from original work [paulruvolo/SoftDesSp16Prep](https://github.com/paulruvolo/SoftDesSp16Prep)
by Paul Ruvolo at Olin College,
extended at [osteele/assignment-tools](https://github.com/osteele/assignment-tools).

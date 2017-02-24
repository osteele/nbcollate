# nbcollate
### Jupyter notebook collation

The **nbcollate** library combines a set of Jupyter notebooks into a single notebook.

## Status

This package is in an alpha state. The API may change.

Remaining work includes:

- [ ] current algorithm misses response cells
- [ ] documentation
- [ ] command-line interface
- [ ] option to concatenate
- [ ] parameterize prompt recognition

## Related Projects

[classroom-tools](https://github.com/olin-computing/classroom-tools) scripts related to using GitHub and Jupyter in education, including a command-line version of an older version of this code. That script will eventually be modified to use this package.

A web application with similar functionality is at [osteele/assignment-dashboard](https://github.com/osteele/assignment-dashboard). That application caches the state of GitHub into a local sqlite3 store, and provides a web interface for inspect completion status by student or by question and for browsing the original and collated notebooks. That application will eventually be modified to use this package.

## Contributions

This package is derived from original work [paulruvolo/SoftDesSp16Prep](https://github.com/paulruvolo/SoftDesSp16Prep)
by Paul Ruvolo at Olin College,
extended at [osteele/assignment-tools](https://github.com/osteele/assignment-tools).

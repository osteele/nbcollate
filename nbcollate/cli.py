#!/usr/bin/env python
"""nbcollate combines a set of Jupyter notebooks into a single notebook.

Command-line interface for nbcollate.
"""

import argparse
import os
import sys

import nbformat
from . import nbcollate

Parser = argparse.ArgumentParser(description="Create a combined notebook.")
Parser.add_argument('notebook_files', nargs='+', metavar='NOTEBOOK_FILE')


def main():
    args = Parser.parse_args(sys.argv[1:])
    # print(args.notebook_files)
    nbs = [nbformat.read(nbf, as_version=4) for nbf in args.notebook_files]
    # snbs = {i: nb for i, nb in}
    snbs = nbs[1:]
    nb = nbcollate(nbs[0], snbs)
    suffix = "-combined"
    root, ext = os.path.splitext(args.notebook_files[0])
    out = "{}{}{}".format(root, suffix, ext)
    print(out)
    with open(out, 'w') as fp:
        nbformat.write(nb, fp)
    # print(nb)

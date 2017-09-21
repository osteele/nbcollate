#!/usr/bin/env python
"""nbcollate combines a set of Jupyter notebooks into a single notebook.

Command-line interface for nbcollate.
"""

import argparse
import logging
import os
import sys

import nbformat
from . import nbcollate, nb_add_metadata

Parser = argparse.ArgumentParser(description="Create a combined notebook.")
Parser.add_argument('-v', '--verbose', action='store_true')
Parser.add_argument('notebook_files', nargs='+', metavar='NOTEBOOK_FILE')


def main():
    args = Parser.parse_args(sys.argv[1:])
    if args.verbose:
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    nbs = [nbformat.read(nbf, as_version=4) for nbf in args.notebook_files]
    anb = nbs[0]
    nb_add_metadata(anb)
    snbs = nbs[1:]
    nb = nbcollate(nbs[0], snbs)
    suffix = "-combined"
    root, ext = os.path.splitext(args.notebook_files[0])
    out = "{}{}{}".format(root, suffix, ext)
    with open(out, 'w') as fp:
        nbformat.write(nb, fp)

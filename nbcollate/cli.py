#!/usr/bin/env python
"""Create a combined notebook. The first path is the assignment notebook.
Remaining paths are student notebooks.
"""

import argparse
import logging
import os
import sys

import nbformat
import nbformat.reader
import nbcollate as nbc
from . import nbcollate, nb_add_metadata


def safe_read(nbf):
    """A wrapper from nbformat.read, that prints a warning and returns None on
    bad notebooks.
    """
    try:
        return nbformat.read(nbf, as_version=4)
    except nbformat.reader.NotJSONError:
        print('while reading', nbf)


def collate(master_nb_path, student_nb_paths, args):
    """Collate notebooks.

    Arguments
    ---------
    nb_files: [str]
        A list of notebook file pathnames.
    """
    if args.verbose:
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    student_nbs = [safe_read(nbf) for nbf in student_nb_paths]
    student_nbs = [collated_nb for collated_nb in student_nbs if collated_nb]
    master_nb = safe_read(master_nb_path)
    assert master_nb
    nb_add_metadata(master_nb)
    collated_nb = nbcollate(master_nb, student_nbs)
    suffix = "-combined"
    root, ext = os.path.splitext(args.notebook_files[0])
    collated_nb_path = "{}{}{}".format(root, suffix, ext)
    if args.out:
        collated_nb_path = os.path.join(
            args.out, os.path.split(collated_nb_path)[1])
    if not args.force and os.path.exists(collated_nb_path):
        # FIXME raise condition; instead open w/ os.O_CREAT | os.O_WRONLY
        err = FileExistsError()
        err.filename = collated_nb_path
        raise err
    if not args.dry_run:
        with open(collated_nb_path, 'w') as fp:
            nbformat.write(collated_nb, fp)
    print('wrote', collated_nb_path)


def main(args=sys.argv[1:]):
    """Create a collated notebook."""
    parser = argparse.ArgumentParser(description=__doc__)
    nb_nargs = '*' if '--version' in args else '+'
    parser.add_argument('-f', '--force', type=str,
                        help="Force overwrite existing file")
    parser.add_argument('-n', '--dry-run', help="Dry run")
    parser.add_argument('-o', '--out', type=str, help="Output directory")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--version', action='store_true')
    parser.add_argument('notebook_files', nargs=nb_nargs,
                        metavar='NOTEBOOK_FILE')
    args = parser.parse_args(args)
    if args.version:
        print('nbcollate version', nbc.__version__)
        return
    nb_files = args.notebook_files
    if not nb_files:
        parser.error(
            'the following arguments are required: NOTEBOOK_FILE')
    try:
        collate(nb_files[0], nb_files[1:], args)
    except FileExistsError as e:
        sys.stderr.write(
            "Output file already exists. Repeat with --force to replace it.\n")
        sys.exit(1)

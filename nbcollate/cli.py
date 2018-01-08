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
from . import nbcollate


def safe_read(nbf):
    """A wrapper for nbformat.read, that prints a warning and returns None on
    bad notebooks.
    """
    try:
        return nbformat.read(nbf, as_version=4)
    except nbformat.reader.NotJSONError:
        print('while reading', nbf)


def capitalize(s):
    return s[:1].upper() + s[1:]


def collate(master_nb_path, submission_paths, args):
    """Collate notebooks.

    Arguments
    ---------
    master_nb_path: str
        The master notebook.
    submission_paths: [str]
        A list of notebook file pathnames.
    """
    if args.verbose:
        logging.basicConfig(format='%(message)s', level=logging.INFO)
    submission_nbs = [safe_read(nbf) for nbf in submission_paths]
    submission_nbs = [collated_nb for collated_nb in submission_nbs if collated_nb]
    master_nb = safe_read(master_nb_path)
    assert master_nb
    labels = None
    if args.label:
        labels = [capitalize(os.path.splitext(os.path.split(f)[1])[0].replace('-', ' '))
                  for f in submission_paths]

    collated_nb = nbcollate(master_nb, submission_nbs, labels=labels)
    if not args.label:
        nbc.remove_duplicate_answers(collated_nb)
        # nbc.sort_answers(collated_nb)

    suffix = "-collated"
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
        with open(collated_nb_path, 'w') as f:
            nbformat.write(collated_nb, f)
    print('wrote', collated_nb_path)


def main(args=sys.argv[1:]):
    "Create a collated notebook."
    parser = argparse.ArgumentParser(description=__doc__)
    nb_nargs = '*' if '--version' in args else '+'
    parser.add_argument('-f', '--force', action='store_true', help="Force overwrite existing file")
    parser.add_argument('-n', '--dry-run', help="Dry run")
    parser.add_argument('-o', '--out', type=str, help="Output directory")
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--label', action='store_true', help="Label answers by notebook")
    parser.add_argument('--version', action='store_true')
    parser.add_argument('notebook_files', nargs=nb_nargs, metavar='NOTEBOOK_FILE')
    args = parser.parse_args(args)
    if args.version:
        print('nbcollate version', nbc.__version__)
        return
    if not args.notebook_files:
        parser.error('the following arguments are required: NOTEBOOK_FILE')
    master_file, *submission_files = args.notebook_files
    # Remove the master file from the answer files. This allows the CLI
    # to be used in the pattern `nbcollate master.ipynb *.ipynb`.
    if master_file in submission_files:
        submission_files = [f for f in submission_files if f != master_file]
    try:
        collate(master_file, submission_files, args)
    except FileExistsError:
        sys.stderr.write("Output file already exists. Repeat with --force to replace it.\n")
        sys.exit(1)

"""Collate an assignment and answer Jupyter notebooks into a single notebook.

This script is designed to support active reading.  It takes as input
a set of Jupyter notebooks as well as some target cells which define a set
of reading exercises.  The script processes the collection of notebooks
and builds a notebook which summarizes the responses to each question.

Based on work by Paul Ruvolo.
Rewritten by Oliver Steele
"""

import re
# from collections import Iterable, OrderedDict
from collections import namedtuple
from difflib import SequenceMatcher
from itertools import starmap

import nbformat
# from cached_property import cached_property
# from numpy import argmin

# QUESTION_RE = r'#+ (Exercise|Question)'


def nb_clear_outputs(nb):
    """Clear the output cells from a Jupyter notebook."""
    for cell in nb.cells:
        if 'outputs' in cell:
            cell['outputs'] = []


def nbcollate(assignment_nb, submission_nbs, *, ids=None, names=None, clear_outputs=False):
    """Create a notebook based on assignment_nb, that incorporates answers from student_nbs.

    Args:
        assignment_nb: a Jupyter notebook with the assignment
        student_nbs: a dict or iterable whose values are notebooks with answers

    Returns:
        A Jupyter notebook
    """
    if isinstance(submission_nbs, dict):
        assert not ids
        ids = list(submission_nbs.keys())
        submission_nbs = list(submission_nbs.values())

    def label_cell(s_name):
        return nbformat.v4.new_markdown_cell(source='**{}**'.format(s_name))
    Opcode = namedtuple('opcode', ['op', 'i1', 'i2', 'j1', 'j2'])
    changes = sorted((oc.i2, i, oc, nb.cells[oc.j1:oc.j2])
                     for i, nb in enumerate(submission_nbs)
                     for oc in starmap(Opcode, NotebookMatcher(assignment_nb, nb).get_opcodes()))
    output_cells = assignment_nb.cells[:]
    di = 0
    for _, i, opcode, b_cells in changes:
        op, i1, i2, j1, j2 = opcode
        if op in ('insert', 'replace'):
            i0 = i2 + di
            if ids:
                for c in b_cells:
                    c.metadata.nbcollate_source = ids[i]
            if names:
                b_cells = [label_cell(names[i])] + b_cells
            output_cells[i0:i0] = b_cells
            di += len(b_cells)
    nb = assignment_nb.copy()
    nb.cells = [c for c in output_cells if c.source.strip()]
    if clear_outputs:
        nb_clear_outputs(nb)
    return nb


def cell_strings(nb):
    return [cell.source.strip() for cell in nb.cells]


def NotebookMatcher(nb1, nb2):
    return SequenceMatcher(None, cell_strings(nb1), cell_strings(nb2))


def isections(nb):
    section = (None, [])
    for cell in nb.cells:
        m = re.match(r'^##+\s*(.+)', cell.source)
        if m:
            if section[-1]:
                yield section
            section = (m.group(1), [])
        section[-1].append(cell)
    if section[-1]:
        yield section


def remove_duplicate_answers(nb):
    dups = []
    for _, cells in isections(nb):
        seen = set()
        for c in cells:
            h = c.source.strip()
            if h in seen:
                dups.append(c)
            seen.add(h)
    for d in dups:
        nb.cells.remove(d)


def sort_answers(nb):
    dups = []
    out = []
    for _, cells in isections(nb):
        out += sorted(cells, key=lambda c: len(c.source.splitlines()))
    nb.cells = out


def get_cell_source_id(cell):
    return getattr(cell.metadata, 'nbcollate_source', None)


def get_answer_tuples(nb):
    "Return a set of tuples (student_id, prompt_title) of answered prompts."
    return {(title, get_cell_source_id(c))
            for title, cells in isections(nb)
            for c in cells if get_cell_source_id(c) is not None}

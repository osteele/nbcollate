import os
import re
from collections import OrderedDict

import nbformat

from nbcollate import nb_add_metadata


def read_notebook(basename):
    if not basename.endswith('.ipynb'):
        basename += '.ipynb'
    nb = nbformat.read(os.path.join(os.path.dirname(__file__), 'files', basename), as_version=4)
    nb_add_metadata(nb)
    return nb


def maybe_write_notebook(nb, basename):
    if not os.environ.get('PYTEST_SAVE_OUTPUTS', False):
        return
    if not basename.endswith('.ipynb'):
        basename += '.ipynb'
    output_path = os.path.join(os.path.dirname(__file__), 'build', basename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    nbformat.write(nb, open(output_path, 'w'))


# maybe some of this should be exposed from, or moved to, the package itself
def nb_sections(nb):
    sections = OrderedDict()
    section = []
    for cell in nb.cells:
        if cell.cell_type == 'markdown' and cell.source.startswith('#'):
            m = re.match(r'#+\s*(.*)', cell.source)
            assert m
            section = []
            sections[m.group(1)] = section
        section.append(cell)
    return sections


# TODO make this a matcher or something
def section_contains_string(sections, section_name, text):
    return any(text in cell.source for cell in sections[section_name])

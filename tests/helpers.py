import itertools
import os
import re
from collections import OrderedDict, namedtuple

import nbformat


def read_notebook(basename):
    """"Read notebook `basename` from the test files directory."""
    if not basename.endswith('.ipynb'):
        basename += '.ipynb'
    nb = nbformat.read(
        os.path.join(os.path.dirname(__file__), 'files', basename),
        as_version=4)
    return nb


def maybe_write_notebook(nb, basename):
    """If PYTEST_SAVE_OUTPUTS is set, save the notebook to test/build/{basename}.ipynb."""
    if not os.environ.get('PYTEST_SAVE_OUTPUTS',
                          False) not in {False, "0", "false"}:
        return
    if not basename.endswith('.ipynb'):
        basename += '.ipynb'
    output_path = os.path.join(os.path.dirname(__file__), 'build', basename)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    nbformat.write(nb, open(output_path, 'w'))


class NotebookSection(namedtuple('_NotebookSection', 'title children cells')):
    def __str_lines__(self):
        prefix = '  '
        return itertools.chain(['Section: ' + self.title], (
            prefix + 'cell: ' + repr(cell.source)
            for cell in self.cells), (prefix + line
                                      for child in self.children.values()
                                      for line in child.__str_lines__()))

    def __str__(self):
        return '\n'.join(self.__str_lines__())

    def __contains__(self, title):
        return title in self.children


def nb_sections(nb):
    """Return a tree that represents the sections (by header) of a notebook.

    A Section is a tuple of a (dict, cells), where dict is an OrderedDict
    that maps titles to Sections.
    """

    def next_key(section, title):
        key = title
        if key in parent:
            candidates = map(lambda n: ("%s (%d)" % (key, n)).strip(),
                             itertools.count(1))
            key = next(itertools.filterfalse(parent.__contains__, candidates))
        return key

    path = []
    # import pudb; pu.db
    for cell in nb.cells:
        if cell.cell_type == 'markdown' and cell.source.startswith('#'):
            m = re.match(r'(#+)\s*(.*)', cell.source)
            assert m
            hash_prefix, title = m.groups()
            level = len(hash_prefix)

            while level < len(path) + 1:
                current_section = path.pop()
            while level > len(path):
                current_section = NotebookSection(title
                                                  if level == len(path) + 1
                                                  else '', OrderedDict(), [])
                if path:
                    parent = path[-1]
                    key = next_key(parent, title
                                   if level == len(path) + 1 else '')
                    parent.children[key] = current_section
                path.append(current_section)

        current_section.cells.append(cell)

    return path[0]


# TODO make this a matcher or something
def section_contains_string(nbtree, section_title, text):
    return any(text in cell.source
               for cell in nbtree.children[section_title].cells)


if __name__ == '__main__':
    assignment_nb = read_notebook('assignment')
    sections = nb_sections(assignment_nb)
    print(sections)

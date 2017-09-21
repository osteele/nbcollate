"""Collate an assignment and answer Jupyter notebooks into a single notebook.

This script is designed to support active reading.  It takes as input
a set of ipython notebook as well as some target cells which define a set
of reading exercises.  The script processes the collection of notebooks
and builds a notebook which summarizes the responses to each question.

Original work by Paul Ruvolo.
Adapted by Oliver Steele
"""

# TODO adding and parsing the cell metadata is messy. It dates from when
# the nb author supplied this

import re
from collections import Iterable, OrderedDict
from copy import deepcopy
import logging

import Levenshtein
import nbformat as nbf
from cached_property import cached_property
from numpy import argmin

# Constants
#

# QUESTION_RE = r'#+ (Exercise|Question)'
QUESTION_RE = r'#+ '
POLL_RE = r'#+ .*(poll|Notes for the Instructors|Reading Journal Feedback)'
CLEAR_OUTPUTS = True

# Logging
#

logger = logging.getLogger(__name__)


# Functions
#


def nb_add_metadata(nb):
    """Add metadata to a notebook."""
    for cell in nb.cells:
        if cell.cell_type == 'markdown' and cell.source:
            if re.match(QUESTION_RE, cell.source, re.IGNORECASE):
                cell.metadata['is_question'] = True
            elif re.match(POLL_RE, cell.source, re.IGNORECASE):
                cell.metadata['is_question'] = True
                cell.metadata['is_poll'] = True


def nb_clear_outputs(nb):
    """Clear the output cells from a Jupyter notebook."""
    for cell in nb.cells:
        if 'outputs' in cell:
            cell['outputs'] = []


def nbcollate(assignment_nb, student_nbs, **kwargs):
    """Create a notebook based on assignment_nb, that incorporates answers from student_nbs.

    Args:
        assignment_nb: a Jupyter notebook with the assignment
        student_nbs: a dict or iterable whose values are notebooks with answers

    Returns:
        A Jupyter notebook
    """
    if isinstance(student_nbs, Iterable) and not isinstance(student_nbs, dict):
        student_nbs = dict(enumerate(student_nbs))
    nbe = NotebookCollator(assignment_nb, student_nbs)
    return nbe.get_collated_notebook(**kwargs)


# The extractor
#
from typing import Dict


class NotebookCollator(object):
    """The top-level class for extracting answers from a notebook."""

    MATCH_THRESH = 10  # maximum edit distance to consider something a match

    def __init__(self, notebook_template, notebooks):
        """Initialize with the specified notebook URLs and list of question prompts."""
        self.template = notebook_template
        self.notebooks = notebooks.values()
        self.usernames = notebooks.keys()
        self._processed = False
        nb_add_metadata(notebook_template)

    @cached_property
    def question_prompts(self):
        """Return a list of `QuestionPrompt`.

        Each cell with metadata `is_question` truthy produces an instance of `QuestionPrompt`.
        """
        prompts = []
        prev_prompt = None
        for idx, cell in enumerate(self.template.cells):
            is_final_cell = idx + 1 == len(self.template.cells)
            metadata = cell.metadata
            if metadata.get('is_question', False):
                cell_source = cell.source
                if prev_prompt is not None:
                    prompts[-1].stop_md = cell_source
                is_poll = metadata.get(
                    'is_poll',
                    'Reading Journal feedback' in cell_source.split('\n')[0])
                prompts.append(
                    QuestionPrompt(
                        question_heading='',
                        name=metadata.get('problem', None),
                        index=len(prompts),
                        start_md=cell_source,
                        stop_md='next_cell',
                        is_optional=metadata.get('is_optional', None),
                        is_poll=is_poll))
                if metadata.get('allow_multi_cell', False):
                    prev_prompt = prompts[-1]
                    # if it's the last cell, take everything else
                    if is_final_cell:
                        prompts[-1].stop_md = ''
                else:
                    prev_prompt = None
        logger.info('prompts = %s', prompts)
        return prompts

    def _process(self):
        """Filter the notebook at the notebook_URL so that it only contains the questions and answers to the reading."""
        for prompt in self.question_prompts:
            prompt.answer_status = {}
            for username, notebook in zip(self.usernames, self.notebooks):
                suppress_non_answer = bool(prompt.answers)
                response_cells = \
                    prompt.get_closest_match(notebook.cells,
                                             NotebookCollator.MATCH_THRESH,
                                             suppress_non_answer)
                if not response_cells:
                    status = 'missed'
                elif not response_cells[-1].source or not any(
                        cell.source.strip() for cell in response_cells):
                    status = 'blank'
                else:
                    status = 'answered'
                    if not suppress_non_answer:
                        # If it's the first notebook with this answer, extract the questions from it.
                        # This is kind of a bass-ackwards way to do this; it's incremental from the previous
                        # strategy.
                        prompt.cells = [
                            cell for cell in response_cells
                            if cell.metadata.get('is_question', False)
                        ]
                        response_cells = [
                            cell for cell in response_cells
                            if cell not in prompt.cells
                        ]
                    prompt.answers[username] = response_cells
                prompt.answer_status[username] = status

        self._processed = True

        # FIXME doesn't work because questions are collected into first response
        # sort_responses = not self.include_usernames
        # if sort_responses:
        #     def cell_slines_length(response_cells):
        #         return len('\n'.join(cell['source') for cell in response_cells).strip())
        #     for prompt in self.question_prompts:
        # prompt.answers = OrderedDict(sorted(prompt.answers.items(),
        # key=lambda t: cell_slines_length(t[1])))

    def get_collated_notebook(self,
                              clear_outputs=False,
                              include_usernames=False):
        if not self._processed:
            self._process()

        remove_duplicate_answers = not include_usernames
        filtered_cells = []
        for prompt in self.question_prompts:
            filtered_cells += prompt.cells
            answers = prompt.answers_without_duplicates if remove_duplicate_answers else prompt.answers
            for username, response_cells in answers.items():
                if include_usernames:
                    filtered_cells.append(
                        new_markdown_heading_cell(username, 4))
                filtered_cells.extend(response_cells)

        collated_nb = nbf.v4.new_notebook()
        collated_nb.metadata = self.template.metadata
        collated_nb.cells = filtered_cells
        if clear_outputs:
            collated_nb.cells = deepcopy(collated_nb.cells)
            nb_clear_outputs(collated_nb)
        return collated_nb

    def report_missing_answers(self):
        """Return a list of [(question_name, {student_name: answer_status})].

        answer_status is in {'missed', 'blank', 'answered'}.
        """
        if not self._processed:
            self._process()

        return [(prompt.name, prompt.answer_status)
                for prompt in self.question_prompts
                if not prompt.is_poll and not prompt.is_optional]


class QuestionPrompt(object):
    """A QuestionPrompt represents a prompt within an assignment."""

    def __init__(self,
                 question_heading,
                 start_md,
                 stop_md,
                 name=None,
                 index=None,
                 is_poll=False,
                 is_optional=None):
        """Initialize a question prompt.

        Initialize a question prompt with the specified starting markdown (the question), and stopping
        markdown (the markdown from the next content cell in the notebook).  To read to the end of the
        notebook, set stop_md to the empty string.  The heading to use in the summary notebook before
        the extracted responses is contined in question_heading.
        To omit the question heading, specify the empty string.
        """
        if is_optional is None and start_md:
            is_optional = bool(
                re.search(r'optional', start_md.split('\n')[0], re.I))
        self.question_heading = question_heading
        self._name = name
        self.start_md = start_md
        self.stop_md = stop_md
        self.is_optional = is_optional
        self.is_poll = is_poll
        self.index = index
        self.answers = OrderedDict()
        self.cells = []

    @property
    def title(self):
        title = self.start_md
        if title.startswith('#'):
            title = re.match('#+\s*(.*)', title).group(1)
        return title

    def __repr__(self):
        """Return string for use in repr(self)."""
        return "<class {} {!r}>".format(self.__class__.__name__, self.title)

    def __str__(self):
        """Return string for use in str(self)."""
        return self.title

    @property
    def answers_without_duplicates(self):
        answers = dict(self.answers)
        answer_strings = set(
        )  # answers to this question, as strings; used to avoid duplicates
        for username, response_cells in self.answers.items():
            answer_string = '\n'.join(cell.source
                                      for cell in response_cells).strip()
            if answer_string in answer_strings:
                del answers[username]
            else:
                answer_strings.add(answer_string)
        return answers

    @property
    def name(self):
        m = re.match(r'^#+\s*(.+)\n', self.start_md)
        if self._name:
            return self._name
        format_str = {
            (False, False): '',
            (False, True): '{title}',
            (True, False): '{number}',
            (True, True): '{number}. {title}'
        }[isinstance(self.index, int), bool(m)]
        return format_str.format(
            number=(self.index or 0) + 1, title=m and m.group(1))

    def get_closest_match(self,
                          cells,
                          matching_threshold,
                          suppress_non_answer_cells=False):
        """Return a list of cells that most closely match the question prompt.

        If no match is better than matching_threshold return the empty list.
        """
        match = []
        distances = [
            Levenshtein.distance(self.start_md, cell.source) for cell in cells
        ]
        if min(distances) > matching_threshold:
            return match

        best_match = argmin(distances)
        if self.stop_md == 'next_cell':
            end_offset = 2
        elif len(self.stop_md) == 0:
            end_offset = len(cells) - best_match
        else:
            distances = [
                Levenshtein.distance(self.stop_md, cell.source)
                for cell in cells[best_match:]
            ]
            if min(distances) > matching_threshold:
                return match
            end_offset = argmin(distances)

        if len(self.question_heading) != 0 and not suppress_non_answer_cells:
            match.append(new_markdown_heading_cell(self.question_heading, 2))
        if not suppress_non_answer_cells:
            match.append(cells[best_match])
        match.extend(cells[best_match + 1:best_match + end_offset])
        return match


def new_markdown_heading_cell(title, level):
    """Create a Markdown cell with the specified text at the specified heading level.

    E.g. mark_down_heading_cell('Title', 3) -> '### Title'
    """
    return nbf.v4.new_markdown_cell('{:#<{}} {}'.format('', level, title))

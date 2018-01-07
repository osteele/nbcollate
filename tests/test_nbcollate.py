from collections import OrderedDict

from helpers import maybe_write_notebook, nb_sections, read_notebook, section_contains_string
from nbcollate import nbcollate, get_answer_tuples, nb_clear_outputs
import nbcollate as nbc

ASSIGNMENT_NB = read_notebook('assignment')
SUBMISSION_NBS = OrderedDict(
    (student_name, read_notebook(student_name))
    for student_name in ['student-1', 'student-2', 'student-3', 'student-4'])


def test_collate_without_names():
    nb = nbcollate(ASSIGNMENT_NB, SUBMISSION_NBS, clear_outputs=True)
    maybe_write_notebook(nb, 'anonymous.ipynb')

    assert nb.metadata
    assert nb.metadata == ASSIGNMENT_NB.metadata

    sections = nb_sections(nb)

    assert "Question 1" in sections
    assert section_contains_string(sections, "Question 1",
                                   'print("Student 1 answers question 1.")')
    assert section_contains_string(sections, "Question 1",
                                   'print("Student 2 answers question 1.")')
    # assert section_contains_string(sections, "Question 1", 'print("Student 2 answers question 1 with more code.")')
    assert section_contains_string(sections, "Question 1",
                                   'print("Student 3 answers question 1.")')

    assert "Question 2" in sections
    assert section_contains_string(sections, "Question 2",
                                   'print("Student 1 answers question 2.")')
    assert not section_contains_string(
        sections, "Question 2", 'print("Student 2 answers question 2.")')
    assert section_contains_string(sections, "Question 2",
                                   'print("Student 3 answers question 2.")')

    assert "A Quick Poll" in sections
    assert section_contains_string(sections, "A Quick Poll",
                                   'Student 1 answers the quick poll')
    assert section_contains_string(sections, "A Quick Poll",
                                   'Student 2 answers the quick poll')
    assert not section_contains_string(sections, "A Quick Poll",
                                       'Student 3 answers the quick poll')


def assert_golden(nb, basename, clear_outputs=False):
    gm = read_notebook(basename)
    if clear_outputs:
        nb_clear_outputs(gm)
    maybe_write_notebook(nb, basename)
    assert nb == gm


def test_nbcollate_without_labels():
    nb = nbcollate(ASSIGNMENT_NB, SUBMISSION_NBS.values(), clear_outputs=True)
    assert_golden(nb, 'assignment-collated.ipynb', clear_outputs=True)

    nb = nbcollate(ASSIGNMENT_NB, SUBMISSION_NBS.values(), clear_outputs=False)
    assert_golden(nb, 'assignment-collated.ipynb', clear_outputs=False)


def test_nbcollate_sort():
    submission_nbs = [read_notebook('sorted-%d.ipynb' % i) for i in [1, 2]]
    nb = nbcollate(ASSIGNMENT_NB, submission_nbs, clear_outputs=True)
    nbc.sort_answers(nb)
    assert_golden(nb, 'sorted.ipynb', clear_outputs=True)


def test_nbcollate_remove_dups():
    submission_nbs = [read_notebook('dups-%d.ipynb' % i) for i in [1, 2]]
    nb = nbcollate(ASSIGNMENT_NB, submission_nbs, clear_outputs=True)
    nbc.remove_duplicate_answers(nb)
    assert_golden(nb, 'deduped.ipynb', clear_outputs=True)


def test_report_missing_answers():
    answers = get_answer_tuples(nbcollate(ASSIGNMENT_NB, SUBMISSION_NBS))
    assert {title for title, _ in answers} == {'A Quick Poll', 'Question 1', 'Question 2'}
    assert {student for _, student in answers} == {'student-1', 'student-2', 'student-3', 'student-4'}

    assert ('Question 1', 'student-1') in answers
    assert ('Question 1', 'student-2') in answers
    assert ('Question 1', 'student-3') in answers

    assert ('Question 2', 'student-1') in answers
    assert ('Question 2', 'student-2') not in answers
    assert ('Question 2', 'student-3') in answers

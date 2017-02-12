from collections import OrderedDict

from helpers import maybe_write_notebook, nb_sections, read_notebook, section_contains_string
from nbcollate import NotebookExtractor, nbcollate

assignment_nb = read_notebook('assignment')
student_notebooks = OrderedDict((student_name, read_notebook(student_name))
                                for student_name in ['student-1', 'student-2', 'student-3'])


def test_collate_without_names():
    nb = nbcollate(assignment_nb, student_notebooks, clear_outputs=True)
    maybe_write_notebook(nb, 'anonymous.ipynb')

    assert nb.metadata
    assert nb.metadata == assignment_nb.metadata

    sections = nb_sections(nb)

    # Debugging:
    # for section_title, cells in sections.items():
    #     print(section_title)
    #     print('---'.join(c.source for c in cells))

    assert "Question 1" in sections
    assert section_contains_string(sections, "Question 1", 'print("Student 1 answers question 1.")')
    assert section_contains_string(sections, "Question 1", 'print("Student 2 answers question 1.")')
    # assert section_contains_string(sections, "Question 1", 'print("Student 2 answers question 1 with more code.")')
    assert section_contains_string(sections, "Question 1", 'print("Student 3 answers question 1.")')

    assert "Question 2" in sections
    assert section_contains_string(sections, "Question 2", 'print("Student 1 answers question 2.")')
    assert not section_contains_string(sections, "Question 2", 'print("Student 2 answers question 2.")')
    assert section_contains_string(sections, "Question 2", 'print("Student 3 answers question 2.")')

    assert "A Quick Poll" in sections
    assert section_contains_string(sections, "A Quick Poll", 'Student 1 answers the quick poll')
    assert section_contains_string(sections, "A Quick Poll", 'Student 2 answers the quick poll')
    assert not section_contains_string(sections, "A Quick Poll", 'Student 3 answers the quick poll')


def test_collate_with_names():
    nb = nbcollate(assignment_nb, student_notebooks, clear_outputs=True, include_usernames=True)
    maybe_write_notebook(nb, 'named.ipynb')

    # TODO
    # preserves order of responses
    # assert (next(i for i, c in enumerate(sections["Question 1"]) if 'Student 1 answers question 1' in c.source) <
    #         next(i for i, c in enumerate(sections["Question 1"]) if 'Student 2 answers question 1' in c.source))


def test_report_missing_answers():
    nbe = NotebookExtractor(assignment_nb, student_notebooks)
    answer_status = dict(nbe.report_missing_answers())

    assert set(answer_status.keys()) == {'1. Question 1', '2. Question 2'}
    assert answer_status['1. Question 1']['student-1'] == 'answered'
    assert answer_status['1. Question 1']['student-2'] == 'answered'
    assert answer_status['1. Question 1']['student-3'] == 'answered'

    assert answer_status['2. Question 2']['student-1'] == 'answered'
    assert answer_status['2. Question 2']['student-2'] == 'blank'
    assert answer_status['2. Question 2']['student-3'] == 'answered'

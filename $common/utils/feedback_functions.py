#!/usr/bin/python3


from inginious_container_api import feedback, rst


def compute_score(number_of_questions, correct_answers):
    """Set and return the score of the evaluated submission.

    :param number_of_questions: the number of task that composes the current problem
    :type number_of_questions: int
    :param correct_answers: the number of task that passed the correction successfully
    :type correct_answers: float
    """

    score = 0.0
    if correct_answers != 0:
        score = 100.0 / number_of_questions * correct_answers
    feedback.set_grade(score)
    return score


def append_raw_html_feedback(content, task=None, title="Encadré ci-dessous, le résultat de votre soumission:", is_file=False):
    """Insert feedback as a note Admonitions (see `INGInious documentation <https://docs.inginious.org/en/latest/teacher_doc/rst.html#admonitions-warnings-tips>`_ ) nested in the main box.

    :param content: HTML code to render in the feedback
    :type content: str
    :param task: task name in case of a task-specific feedback
    :type task: str
    :param title: the Admonition title
    :type title: str
    :param is_file: helps determine if `content` should be treated as a str or as a filename
    :type is_file: bool
    """

    code_fb = ""
    if is_file:
        with open(content, "r") as f:
            string_fb = f.read()
    else:
        code_fb = content

    deindentation = rst.indent_block(-2, "\n\n", "\t")
    indented_title = rst.indent_block(1, f":title: {title}\n\n", "\t")
    indented_raw_directive = rst.indent_block(1, "\n\n.. raw:: html\n\n", "\t")

    indented_code = rst.indent_block(2, code_fb.strip(), "\t") # Indent the HTML code with 1 unit of tabulations
    if task is None:
        feedback.set_global_feedback("\n\n.. note::\n" + indented_title, True)
        feedback.set_global_feedback(indented_raw_directive + indented_code.rstrip(), True) # Appends the block to the global feedback
    else:
        feedback.set_problem_feedback("\n\n.. note::\n" + indented_title, task, True)
        feedback.set_problem_feedback(indented_raw_directive + indented_code.rstrip(), task, True)



def append_tip_feedback(content, task=None, title="Tips"):
    """Insert feedback as a tip Admonitions (see `INGInious documentation <https://docs.inginious.org/en/latest/teacher_doc/rst.html#admonitions-warnings-tips>`_ ) nested in the main box.

    :param content: HTML code to render in the feedback
    :type content: str
    :param task: task name in case of a task-specific feedback
    :type task: str
    :param title: the Admonition title
    :type title: str
    """

    indented_title = rst.indent_block(1, f":title: {title}\n\n", "\t")
    indented_fb = rst.indent_block(1, content.strip(), "\t")

    if task is None:
        feedback.set_global_feedback("\n\n.. tip::\n" + indented_title, True)
        feedback.set_global_feedback(indented_fb, True) # Appends the block to the global feedback
    else:
        feedback.set_problem_feedback("\n\n.. tip::\n" + indented_title, task, True)
        feedback.set_problem_feedback(indented_fb.rstrip(), task, True)


if __name__ == "__main__":
    pass
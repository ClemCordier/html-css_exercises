#!/usr/bin/python3

import sys
sys.path.append("/course/common/utils")
from inginious_container_api import input, feedback, rst
from answer import expected_answers
from feedback_functions import *
from validation_functions import *
from parsing_functions import *
from correction_functions import *

correct_answers = 0
student_answer_q1 = input.get_input("h1_border_color").strip()
student_answer_q2 = input.get_input("precise_border_color").strip()

input.parse_template("template_q1.css")
input.parse_template("template_q2.css")

raw_student_answers = {"h1_border_color": student_answer_q1, "precise_border_color": student_answer_q2}

validation_errors_q1 = css_validator_validation("template_q1.css", task="h1_border_color")
validation_errors_q2 = css_validator_validation("template_q2.css", task="precise_border_color")

validation_errors = {"h1_border_color": validation_errors_q1, "precise_border_color": validation_errors_q2}

for task in validation_errors:
    if validation_errors[task]:
        raw_student_answers.pop(task) # removes non valid response
        for error in validation_errors[task]:
            line_info = f"Ligne {error.get('line_number')}: "
            feedback.set_problem_feedback(f"- {line_info}{error.get('message')}\n", task, True)

parsed_answers = parse_css_as_dict(raw_student_answers)

task_result = check_css_correctness(parsed_answers, expected_answers)

for task in task_result:
    if task_result.get(task):
        correct_answers += 1
        if task == "precise_border_color":
            append_tip_feedback(
                r"""
                Notez que la représentation de couleur utilisée ici ne peut pas être réécrite de façon abrégée, étant donné la paire de composante de rouge qui utilise 2 nombres distincts (:math:`B \neq E`).
                """, task
            )
if correct_answers == 2:
    feedback.set_global_result("success")
    append_tip_feedback(
        """
        Vous aurez certainement remarqué la présence de la propriété ``border-style``.

        Par défaut, sa valeur est définie à ``none``, ce qui correspond à n'afficher aucune bordure.

        Il est donc nécessaire de la redéfinir au préalable afin que notre propriété ``border-color`` soit prise en compte.
        """
    )
else:
    feedback.set_global_result("failed")

compute_score(2, correct_answers)

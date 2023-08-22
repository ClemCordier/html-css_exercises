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
student_answer_q1 = input.get_input("percentage").strip()
student_answer_q2 = input.get_input("alpha").strip()

input.parse_template("template_q1.css") # for validation
input.parse_template("template_q2.css") # for validation

raw_student_answers = {"percentage": student_answer_q1, "alpha": student_answer_q2}

validation_errors_q1 = css_validator_validation("template_q1.css", task="percentage")
validation_errors_q2 = css_validator_validation("template_q2.css", task="alpha")

validation_errors = {"percentage": validation_errors_q1, "alpha": validation_errors_q2}
for task in validation_errors:
    if validation_errors[task]:
        feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", task, True)
        raw_student_answers.pop(task) # removes non valid response
        for error in validation_errors[task]:
            line_info = f"Ligne {error.get('line_number')}: "
            feedback.set_problem_feedback(f"- {line_info}{error.get('message')}\n", task, True)

parsed_answers = parse_css_as_dict(raw_student_answers)

task_result = check_css_correctness(parsed_answers, expected_answers)

for task in task_result:
    if task_result.get(task):
        correct_answers += 1

compute_score(2, correct_answers)
if correct_answers == 2:
    feedback.set_global_result("success")
    append_tip_feedback(
        """
        Il n'y a pas de "meilleure" notation à proprement parler, mais il est toutefois de bon usage de ne pas varier sans cesse les notations afin de préserver une certaine cohérence et lisibilité au sein de votre code.

        Vous êtes donc libre d'utiliser la notation qui vous convient le mieux dans vos futurs projets !
        """
    )
else:
    feedback.set_global_result("failed")
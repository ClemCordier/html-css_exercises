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
student_answer_q1 = input.get_input("date_number")
student_answer_q2 = input.get_input("step")
student_answer_q3 = input.get_input("checkbox")

input.parse_template("template_q1.html")
input.parse_template("template_q2.html")
input.parse_template("template_q3.html")

raw_student_answers = {"date_number": [student_answer_q1, False], "step": [student_answer_q2, False], "checkbox": [student_answer_q3, False]}

validation_errors_q1 = nu_checker_validation("template_q1.html", task="date_number", offset=7)
validation_errors_q2 = nu_checker_validation("template_q2.html", task="step", offset=7)
validation_errors_q3 = nu_checker_validation("template_q3.html", task="checkbox", offset=7)

validation_errors = {"date_number": validation_errors_q1, "step": validation_errors_q2, "checkbox": validation_errors_q3}
for task in validation_errors:
    if validation_errors[task]:
        raw_student_answers.pop(task)
        feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", task, True)
        for error in validation_errors[task]:
            feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : {error.get('message')}\n", task, True)

parsed_answers = parse_html_as_dict(raw_student_answers)

task_result = check_html_correctness(parsed_answers, expected_answers)

for task in task_result:
    if task_result.get(task):
        correct_answers += 1
        if task == "date_number":
            feedback.set_problem_feedback(
                """
                Malgré l'attrait que l'on pourrait avoir, l'utilisation de l'élément ``input`` de type "date" n'est pas toujours la meilleure solution à cause du manque de prise en charge des versions plus anciennes de certains navigateurs.
                """, task, True
            )
        elif task == "step":
            append_tip_feedback(
                """
                "*Never trust user input*"

                Dès lors que l'on traite des données utilisateurs, il est bon d'adopter un état d'esprit préventif: imaginer les pires éventualités afin d'anticiper les entrées invalides et les gérer en amont.
                """, task
            )
        elif task == "checkbox":
            pass


if correct_answers == 3:
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

compute_score(3, correct_answers)

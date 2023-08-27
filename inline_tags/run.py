#!/usr/bin/python3

import sys
sys.path.append("/course/common/utils")
from inginious_container_api import input, feedback, rst
from answer import expected_answers
from feedback_functions import *
from validation_functions import *
from parsing_functions import *
from correction_functions import *


student_answer_q1 = input.get_input("em")
student_answer_q2 = input.get_input("strong")

input.parse_template("template_q1.html")
input.parse_template("template_q2.html")

correct_answers = 0

raw_student_answers = {"em": [student_answer_q1, False], "strong": [student_answer_q2, False]}

validation_errors_q1 = nu_checker_validation("template_q1.html", offset=7)
validation_errors_q2 = nu_checker_validation("template_q2.html", offset=7)

validation_errors = {"em": validation_errors_q1, "strong": validation_errors_q2}

for task in validation_errors:
    if validation_errors[task]:
        raw_student_answers.pop(task)
        feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", task, True)
        for error in validation_errors[task]:
            feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : {error.get('message')}\n", task, True)

# * parsing step
parsed_answers = parse_html_as_dict(raw_student_answers)

# * correction step
task_result = check_html_correctness(parsed_answers, expected_answers)

# * append feedback to successfully answered task
for task in task_result:
    if task_result.get(task):
        correct_answers += 1
        if task == "em":
            append_raw_html_feedback(student_answer_q1, task="em")

        elif task == "strong":
            append_raw_html_feedback(student_answer_q2, task="strong")


compute_score(2, correct_answers)

if correct_answers == 2:
    feedback.set_global_result("success")
    append_tip_feedback(
        """
        HTML possède aussi les éléments ``i`` et ``b`` qui ont respectivement le même rendu visuel que ``em`` et ``strong``: ils transforment  le texte en italique/gras.

        On pourrait légitimement se poser la question: pourquoi existe-t'il plusieurs éléments HTML ayant le même rendu ?

        Pour en comprendre la raison, il faut se rappeler du **rôle de l'HTML: organiser, structurer une page web.**
        Pour cela, on utilise divers éléments, chacun ayant sa propre sémantique.

        L'apparence de notre page, quant à elle, sera gérée par le langage CSS que nous aborderons dans la suite du cours.

        La sémantique des éléments ``i`` et ``b`` n'est donc simplement pas la même que celle des éléments ``em`` et ``strong`` que nous venons de voir.
        """
    )
else:
    feedback.set_global_result("failed")

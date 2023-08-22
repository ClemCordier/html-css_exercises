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
student_answer_q1 = input.get_input("top")
student_answer_q2 = input.get_input("section")

input.parse_template("template_q1.html")
input.parse_template("template_q2.html")

raw_student_answers = {"top": [student_answer_q1, False], "section": [student_answer_q2, False]}

validation_errors_q1 = nu_checker_validation("template_q1.html", task="top", offset=7)
validation_errors_q2 = nu_checker_validation("template_q2.html", task="section", offset=7)

validation_errors = {"top": validation_errors_q1, "section": validation_errors_q2}
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

compute_score(2, correct_answers)
if correct_answers == 2:
    feedback.set_global_result("success")
    append_tip_feedback(
        """
        Un site web est souvent composé de multiples pages, chacune correspondant à un document HTML différent.

        L'élément d'ancre permet de naviguer entre ces pages.

        Pour cela, on renseigne le chemin relatif vers la page en question à l'attribut ``href``, tout comme on le ferait avec l'attribut ``src`` pour une image stockée en local.

        .. raw:: html

            Cliquez sur <a href="link_tags_continued/index.html">le lien suivant</a> afin d'observer cette redirection (interne) entre pages.

        """
    )
else:
    feedback.set_global_result("failed")

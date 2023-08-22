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
student_answer_q1 = input.get_input("audio1")
student_answer_q2 = input.get_input("audio2")
student_answer_q3 = input.get_input("audio3")
student_answer_q4 = input.get_input("video")

input.parse_template("template_q1.html")
input.parse_template("template_q2.html")
input.parse_template("template_q3.html")
input.parse_template("template_q4.html")

raw_student_answers = {"audio1": [student_answer_q1, False], "audio2": [student_answer_q2, False], "audio3": [student_answer_q3, False], "video": [student_answer_q4, False]}

validation_errors_q1 = nu_checker_validation("template_q1.html", task="audio1", offset=7)
validation_errors_q2 = nu_checker_validation("template_q2.html", task="audio2", offset=7)
validation_errors_q3 = nu_checker_validation("template_q3.html", task="audio3", offset=7)
validation_errors_q4 = nu_checker_validation("template_q4.html", task="video", offset=7)

validation_errors = {"audio1": validation_errors_q1, "audio2": validation_errors_q2, "audio3": validation_errors_q3, "video": validation_errors_q4}
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
        if task == "audio3":
            feedback.set_problem_feedback(
                """
                De nos jours, l'élément ``audio`` est pris en charge par une vaste majorité des navigateurs modernes. On pourrait donc se demander l'intérêt d'inclure du texte alternatif.

                Il n'en reste pas moins une bonne pratique de toujours anticiper les "scénarios catastrophes" lorsque l'on code.
                """, task, True
            )
        if task == "video":
            append_tip_feedback(
                """
                Une différence toutefois entre les éléments ``video`` et ``audio``: Ce dernier n'étant pas considéré comme du contenu visuel, il n'accepte pas les attributs de dimension ``width`` & ``height`` (contrairement à ``video``).
                """, task
            )
compute_score(4, correct_answers)
if correct_answers == 4:
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

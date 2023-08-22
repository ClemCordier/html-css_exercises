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
input.parse_template("template.html")
student_answer_q1 = input.get_input("list_tags")
if student_answer_q1 == "0":
    correct_answers += 1
    feedback.set_problem_feedback("Bonne réponse!", "list_tags")
    feedback.set_problem_result("success", "list_tags")
else:
    feedback.set_problem_feedback("Mauvaise réponse", "list_tags")
    feedback.set_problem_result("failed", "list_tags")

student_answer_q2 = input.get_input("list_items").strip().casefold()
student_answer = {"list_items": [student_answer_q2, False]}


validation_errors_q2 = nu_checker_validation("template.html",task="list_items", offset=7)
validation_errors = {"list_items": validation_errors_q2}

tag_errors_q2 = html_tags_validation(student_answer_q2)

if validation_errors_q2:
    feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", "list_items", True)
    for error in tag_errors_q2:
        feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : {error.get('message')}\n", "list_items", True)

elif tag_errors_q2:
    feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", "list_items", True)
    for error in tag_errors_q2:
        feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : l'élément ``{error.get('element')}`` en position n°{error.get('element_number')} dans la hiérarchie ne semble pas être accompagné de sa balise fermante.\n", "list_items", True)

else:
    parsed_student_answer = parse_html_as_dict(student_answer)

    task_result = check_html_correctness(parsed_student_answer, expected_answers)

    for task in task_result:
        if task_result.get(task):
            correct_answers += 1
        else:
            if task == "list_items":
                feedback.set_problem_feedback("\nIci, l'ordre de la liste a une importance particulière. Pensez donc à vous servir de l'élément de liste adéquat !", task, True)


if correct_answers == 2:
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

compute_score(2, correct_answers)

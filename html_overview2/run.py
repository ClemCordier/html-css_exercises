#!/usr/bin/python3

import sys
sys.path.append("/course/common/utils")
from inginious_container_api import input, feedback, rst
from answer import expected_answers
from feedback_functions import *
from validation_functions import *
from parsing_functions import *
from correction_functions import *

input.parse_template("template.html")
answer_q1 = input.get_input("recipe")

raw_student_answers = {"recipe": [answer_q1, False]}

validation_errors = nu_checker_validation("template.html", task="recipe", offset=7)
tag_errors = html_tags_validation(answer_q1)

if validation_errors:
    feedback.set_grade(0.0)
    raw_student_answers.pop("recipe")
    feedback.set_global_result("failed")
    feedback.set_problem_result("failed", "recipe")
    feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", "recipe", True)
    for error in validation_errors:
        feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : {error.get('message')}\n", "recipe", True)

elif tag_errors:
    feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", "recipe", True)
    for error in tag_errors:
        feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : l'élément ``{error.get('element')}`` en position n°{error.get('element_number')} dans la hiérarchie ne semble pas être accompagné de sa balise fermante.\n", "recipe", True)
else:
    parsed_student_answer = parse_html_as_dict(raw_student_answers)

    task_result = check_html_correctness(parsed_student_answer, expected_answers)

    if task_result["recipe"] == True:
        feedback.set_global_result("success")
    else:
        feedback.set_global_result("failed")

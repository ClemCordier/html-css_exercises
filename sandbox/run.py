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
student_answer_q1 = input.get_input("multicursor").strip()

input.parse_template("template_q1.html")

validation_errors_q1 = nu_checker_validation("template_q1.html", offset=7)

raw_student_answers = {"multicursor": [student_answer_q1, False]}

if validation_errors_q1:
    raw_student_answers.pop("multicursor") # removes non valid response
    feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", "multicursor", True)
    for error in validation_errors_q1:
        feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : {error.get('message')}\n", "multicursor", True)

parsed_answers = parse_html_as_dict(raw_student_answers)

task_result = check_html_correctness(parsed_answers, expected_answers)

for task in task_result:
    if task_result.get(task):
        correct_answers += 1


if correct_answers == 1:
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

compute_score(1, correct_answers)
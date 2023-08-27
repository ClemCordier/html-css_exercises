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
student_answer_q1 = input.get_input("tr_td_tags")
student_answer_q2 = input.get_input("th_tag")
student_answer_q3 = input.get_input("span")

input.parse_template("template_q1.html")
input.parse_template("template_q2.html")
input.parse_template("template_q3.html")


raw_student_answers = {"tr_td_tags": [student_answer_q1, False], "th_tag": [student_answer_q2, False], "span": [student_answer_q3, False]}

validation_errors_q1 = nu_checker_validation("template_q1.html", task="tr_td_tags", offset=7)
validation_errors_q2 = nu_checker_validation("template_q2.html", task="th_tag", offset=7)
validation_errors_q3 = nu_checker_validation("template_q3.html", task="span", offset=7)

validation_errors = {"tr_td_tags": validation_errors_q1, "th_tag": validation_errors_q2, "span": validation_errors_q3}
for task in validation_errors:
    if validation_errors[task]:
        raw_student_answers.pop(task)
        feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", task, True)
        for error in validation_errors[task]:
            feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : {error.get('message')}\n", task, True)
    else:
        tag_errors = html_tags_validation(input.get_input(task))
        if tag_errors:
            raw_student_answers.pop(task)
            feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", task, True)
            for error in tag_errors:
                feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : l'élément ``{error.get('element')}`` en position n°{error.get('element_number')} dans la hiérarchie ne semble pas être accompagné de sa balise fermante.\n", task, True)

parsed_answers = parse_html_as_dict(raw_student_answers)

task_result = check_html_correctness(parsed_answers, expected_answers)

for task in task_result:
    if task_result.get(task):
        correct_answers += 1

if correct_answers == 3:
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

compute_score(3, correct_answers)
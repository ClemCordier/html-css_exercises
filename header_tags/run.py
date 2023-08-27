#!/usr/bin/python3

import sys
sys.path.append("/course/common/utils")
import re
from inginious_container_api import input, feedback, rst
from answer import expected_answers
from feedback_functions import *
from validation_functions import *
from parsing_functions import *
from correction_functions import *


answer_q1 = input.get_input("title")
answer_q2 = input.get_input("meta")

correct_answers = 0

raw_student_answers = {"title": [answer_q1, True], "meta": [answer_q2, True]}

# * validation step
validation_errors_q1 = is_invalid_element(answer_q1)
validation_errors_q2 = is_invalid_self_closing_element(answer_q2)

validation_errors = {"title": validation_errors_q1, "meta": validation_errors_q2}
for task in validation_errors:
    if validation_errors[task]:
        raw_student_answers.pop(task) # removes non valid response
        feedback.set_problem_feedback(validation_errors[task], task, True) # append invalid fb msg

# * parsing step
parsed_answers = parse_html_as_dict(raw_student_answers)

# * correction step
task_result = check_html_correctness(parsed_answers, expected_answers)

# * append feedback to successfully answered task
for task in task_result:
    if task_result.get(task):
        correct_answers += 1
        # feedback.set_problem_feedback("**Correct!**\n\n", task, True)
        if task == "title":
            imgblock = rst.get_imageblock("src/title_no_encoding.png") # RST block with image
            feedback.set_problem_feedback(
                """
                Voici une illustration du résultat obtenu:\n
                """ + imgblock, task, True
            )
        elif task == "meta":
            imgblock = rst.get_imageblock("src/title_encoding.png") # RST block with image
            feedback.set_problem_feedback(
                """
                Voici une illustration du résultat obtenu:\n
                """ + imgblock, task, True
            )

if correct_answers == 2:
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

compute_score(2, correct_answers)

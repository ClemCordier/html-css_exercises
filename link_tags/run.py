#!/usr/bin/python3

import sys
sys.path.append("/course/common/utils")
from inginious_container_api import input, feedback, rst
from answer import expected_answers
from feedback_functions import *
from validation_functions import *
from parsing_functions import *
from correction_functions import *

student_answer_q1 = input.get_input("a").strip()
student_answer_q2 = input.get_input("a2").strip()
student_answer_q3 = input.get_input("mailto").strip()
student_answer_q4 = input.get_input("tel").strip()

correct_answers = 0

raw_student_answers = {"a": [student_answer_q1, True], "a2": [student_answer_q2, True], "mailto": [student_answer_q3, True], "tel": [student_answer_q4, True]}

validation_errors_q1 = is_invalid_element(student_answer_q1)
validation_errors_q2 = is_invalid_element(student_answer_q2)
validation_errors_q3 = is_invalid_element(student_answer_q3)
validation_errors_q4 = is_invalid_element(student_answer_q4)

validation_errors = {"a": validation_errors_q1, "a2": validation_errors_q2, "mailto": validation_errors_q3, "tel": validation_errors_q4}
for task in validation_errors:
    if validation_errors[task]:
        raw_student_answers.pop(task) # removes non valid response
        feedback.set_problem_feedback(validation_errors[task], task, True) # append invalid fb msg

parsed_answers = parse_html_as_dict(raw_student_answers)

task_result = check_html_correctness(parsed_answers, expected_answers)

for task in task_result:
    if task_result.get(task):
        correct_answers += 1
        append_raw_html_feedback(input.get_input(task).strip(), task)

if correct_answers == 4:
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

compute_score(4, correct_answers)

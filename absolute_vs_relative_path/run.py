#!/usr/bin/python3

import sys
sys.path.append("/course/common/utils")
from inginious_container_api import input, feedback
from answer import expected_answers
from feedback import feedback_messages
from feedback_functions import *
from correction_functions import *

correct_answers = 0
student_answer_q1 = set(input.get_input("qcm1"))
student_answer_q2 = set(input.get_input("qcm2"))
student_answer_q3 = input.get_input("qcm3")
student_answer_q4 = input.get_input("qcm4")

student_answers = {"qcm1": student_answer_q1, "qcm2": student_answer_q2, "qcm3": student_answer_q3, "qcm4": student_answer_q4}

for task, answer in student_answers.items():
    multiple_answer = True if isinstance(answer, set) else False
    check_mcq_correctness(answer, expected_answers[task], task, multiple_answer=multiple_answer)
    if answer == expected_answers[task]:
        correct_answers += 1
    for choice in answer:
        if task in feedback_messages.keys() and choice in feedback_messages[task].keys():
            feedback.set_problem_feedback(f"- {feedback_messages[task][choice]}\n", task, True)

compute_score(4, correct_answers)
if correct_answers == 4:
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")
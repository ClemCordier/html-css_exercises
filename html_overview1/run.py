#!/usr/bin/python3

import sys
sys.path.append("/course/common/utils")
from inginious_container_api import input, feedback, rst
from answer import expected_answers
from feedback import feedback_messages
from feedback_functions import *
from validation_functions import *
from parsing_functions import *
from correction_functions import *


input.parse_template("template.html")

errors = {}
line_offset = 0
line_number = 0
with open("template.html", 'r') as student_f:
    lines = student_f.readlines()
    for line in lines:
        if line.strip() == "":
            line_offset += 1
            continue
        line_number += 1
        possible_answers = expected_answers["skeleton"][line_number-1].strip().split(',')
        is_correct = False
        for answer in possible_answers:
            if line.strip().casefold() == answer.strip().casefold():
                is_correct = True
                break
        if not is_correct:
            errors[line_number] = line_number + line_offset

if errors:
    feedback.set_global_result("failed")
    feedback.set_problem_feedback("Voici des pistes qui pourraient vous aider:\n\n", "skeleton", True)
    for error, line in errors.items():
        feedback.set_problem_feedback(f"- Ligne {line}: {feedback_messages[error]}\n", "skeleton", True)
        feedback.set_grade(100.0/9*(9-len(errors)))
else:
    feedback.set_global_result("success")
    feedback.set_grade(100.0)

#!/usr/bin/python3

import sys
sys.path.append("/course/common/utils")
from inginious_container_api import input, feedback
from answer import expected_answers
from validation_functions import *
from parsing_functions import *
from feedback_functions import *
from correction_functions import *

correct_answers = 0
student_answer_q1 = input.get_input("size_standard_model")
student_answer_q2 = input.get_input("shorthand_properties")
input.parse_template("template_q2.css")
student_answer_q3 = input.get_input("size_standard_model2").strip()


# check_mcq_correctness(student_answer_q1, expected_answers["size_standard_model"], "size_standard_model", multiple_answer=False, debug=False)
if student_answer_q1 == "2":
    feedback.set_problem_feedback("**Correct !**\n\n", "size_standard_model", True)
    feedback.set_problem_result("success", "size_standard_model")
    correct_answers += 1
else:
    feedback.set_problem_feedback("Mauvaise réponse.\n\n", "size_standard_model", True)
    feedback.set_problem_result("failed", "size_standard_model")
    if student_answer_q1 == "0":
        feedback.set_problem_feedback("Les marges ne sont pas comptabilisées dans le modèle de boîte standard.\n\n", "size_standard_model", True)
    if student_answer_q1 == "1":
        feedback.set_problem_feedback("Les propriétés ``border``, ``margin`` et ``padding`` s'appliquent aux 4 côtés, leur valeur doit donc être prise en compte 2 fois en largeur et 2 fois en hauteur.\n\n", "size_standard_model", True)
    if student_answer_q1 == "3":
        feedback.set_problem_feedback("Hauteur & largeur ne sont pas les seules composantes à intervenir dans le modèle de boîte.\n\n", "size_standard_model", True)

student_answers = {"shorthand_properties": student_answer_q2}
validation_errors_q2 = css_validator_validation("template_q2.css", task="shorthand_properties", offset=0)

if validation_errors_q2:
    student_answers.pop("shorthand_properties")
    feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", "shorthand_properties", True)
    for error in validation_errors_q2:
        line_info = f"Ligne {error.get('line_number')}: "
        feedback.set_problem_feedback(f"- {line_info}{error.get('message')}\n", "shorthand_properties", True)

parsed_answers = parse_css_as_dict(student_answers)

task_result = check_css_correctness(parsed_answers, expected_answers)

for task in task_result:
    if task_result.get(task):
        correct_answers += 1


if student_answer_q3 == "315x160":
    feedback.set_problem_feedback("**Correct !**\n\n", "size_standard_model2", True)
    feedback.set_problem_result("success", "size_standard_model2")
    correct_answers += 1
else:
    feedback.set_problem_feedback("Mauvaise réponse.\n\n", "size_standard_model2", True)
    feedback.set_problem_result("failed", "size_standard_model2")

compute_score(3, correct_answers)
if correct_answers == 3:
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")
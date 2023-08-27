#!/usr/bin/python3

import sys
sys.path.append("/course/common/utils")
from inginious_container_api import input, feedback, rst
from feedback_functions import *
from validation_functions import *
from parsing_functions import *
from correction_functions import *
from answer import expected_answers

correct_answers = 0
student_answer_q1 = input.get_input("lang")
student_answer_q2 = input.get_input("title")

input.parse_template("template_q2.html") # for validation


raw_student_answers = {"title": [student_answer_q2, False]}


validation_errors_q1 = is_invalid_opening_tag(student_answer_q1)
validation_errors_q2 = nu_checker_validation("template_q2.html")
if validation_errors_q1:
    feedback.set_problem_result("failed", "lang")
    feedback.set_problem_feedback(validation_errors_q1, "lang", True)
else:
    is_expected_match = re.fullmatch(r"<html lang\s?=\s?(\"|')fr\1>", student_answer_q1.casefold())
    if is_expected_match:
        correct_answers += 1
        feedback.set_problem_result("success", "lang")
        feedback.set_problem_feedback(f"**Correct!**\n", "lang", True)
    else:
        feedback.set_problem_feedback("Votre réponse n'est pas celle attendue:\n\n", "lang", True)
        match = re.fullmatch(r"<([a-z0-9]+) ([a-z0-9]+)\s?=\s?(\"|')([a-z]+)\3>", student_answer_q1.strip().casefold())
        if match is None:
            feedback.set_problem_feedback(f"- Votre réponse ne semble pas respecter la syntaxe attendue.\n", "lang", True)
        if match.group(1) != "html":
            feedback.set_problem_feedback(f"- ``{match.group(1)}`` ne correspond pas à l'élément attendu.\n", "lang", True)
        if match.group(2) != "lang":
            feedback.set_problem_feedback(f"- ``{match.group(2)}`` ne correspond pas à l'attribut attendu.\n", "lang", True)
        if match.group(4) != "fr":
            feedback.set_problem_feedback(f"- ``{match.group(4)}`` ne correspond pas à la valeur attendue.\n", "lang", True)

if validation_errors_q2:
    raw_student_answers.pop("title")
    feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", "title", True)
    for error in validation_errors_q2:
        feedback.set_problem_feedback(f"- {error.get('message')}\n", "title", True)
else:
    parsed_answers = parse_html_as_dict(raw_student_answers, skip_head=True)

    task_result = check_html_correctness(parsed_answers, expected_answers)

    for task in task_result:
        if task_result.get(task):
            correct_answers += 1
            feedback.set_problem_result("success", task)
            if task == "title":
                append_tip_feedback(
                    """
                    Comme précisé dans l'énoncé de l'exercice, il se peut que l'info-bulle au survol de l'abréviation ne soit pas présent.

                    Les fonctionnalités prises en charge varient d'un navigateur à l'autre (parfois même d'une version à l'autre d'un même navigateur !).

                    Ce genre d'incohérence dans le comportement d'un élément va à l'encontre de l'accessibilité que l'on cherche à optimiser.

                    C'est pourquoi l'utilisation d'un tel attribut doit être fait avec minutie.
                    """, task=task)
                append_raw_html_feedback(student_answer_q2, task=task)

if correct_answers == 2:
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

compute_score(2, correct_answers)

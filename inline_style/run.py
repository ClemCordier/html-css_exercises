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
student_answer_q1 = input.get_input("inline_style").strip()  # for correction purpose

raw_student_answers = {"inline_style": student_answer_q1}

validation_errors_q1 = is_invalid_element(student_answer_q1)

validation_errors = {"inline_style": validation_errors_q1}
for task in validation_errors:
    if validation_errors[task]:
        raw_student_answers.pop(task) # removes non valid response
        feedback.set_problem_feedback(validation_errors[task], task, True) # append invalid fb msg

parsed_answers = parse_inline_css_as_dict(raw_student_answers)
task_result = check_css_correctness(parsed_answers, expected_answers, check_line=False)


for task in task_result:
    if task_result.get(task):
        correct_answers += 1
        if task == "inline_style":
            student_color = parsed_answers[task][0][1]['color']
            translated_color = {"red": "rouge", "green": "verte", "blue": "bleue"}
            append_raw_html_feedback(
                f"""
                <h1 style="color: {student_color};">Le titre de votre site est de couleur: {translated_color[student_color.casefold()]}</h1>
                """
            )

if correct_answers == 1:
    append_tip_feedback(
        """
        Cette première façon d'appliquer du CSS à un document HTML pourrait sembler efficace. Finalement, pourquoi s'embêter si l'on peut styliser nos éléments HTML via des attributs directement ?

        Cette façon de faire est en réalité fortement déconseillée, sauf rare exception: https://developer.mozilla.org/fr/docs/Learn/CSS/First_steps/How_CSS_is_structured#styles_en_ligne
        """
    )
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

compute_score(1, correct_answers)

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

q1 = input.get_input("main_title").strip()
q2 = input.get_input("subtitles").strip()

input.parse_template("template_q1.css")
input.parse_template("template_q2.css")

raw_student_answers = {"main_title": q1, "subtitles": q2}

validation_errors_q1 = css_validator_validation("template_q1.css", task="main_title")
validation_errors_q2 = css_validator_validation("template_q2.css", task="subtitles")

validation_errors = {"main_title": validation_errors_q1, "subtitles": validation_errors_q2}


for task in validation_errors:
    if validation_errors[task]:
        raw_student_answers.pop(task) # removes non valid response
        for error in validation_errors[task]:
            line_info = f"Ligne {error.get('line_number')}: "
            feedback.set_problem_feedback(f"- {line_info}{error.get('message')}\n", task, True)

parsed_answers = parse_css_as_dict(raw_student_answers)

task_result = check_css_correctness(parsed_answers, expected_answers)

for task in task_result:
    if task_result.get(task):
        correct_answers += 1
        if task == "main_title":
            append_tip_feedback(
                """
                Plutôt que d'utiliser un sélecteur d'élément, nous aurions pu ajouter un attribut ``id`` à notre élément ``h1`` et utiliser le sélecteur d'ID associé.

                Cependant, nous avons vu dans la section HTML qu'un élément ``h1`` ne devrait (en principe...) être présent qu'une seule fois par page, rendant l'ajout d'un ID sans intérêt.

                De manière plus général, les sélecteurs d'ID devraient être utilisés avec parcimonie. Favorisez si possible les sélecteurs d'élément ou de classe.
                """, task)
        # elif task == "subtitles":
        #     append_tip_feedback(
        #         """
        #         Plutôt que d'utiliser un sélecteur de classe, nous aurions pu nous contenter d'un sélecteur d'élément étant donné que nous avons assigné la même classe à tous nos éléments ``h2``.

        #         Toutefois, supposons que nous avions prévu d'ajouter des sections supplémentaires à notre page, éléments ``h2`` y compris. Dans ce cas, l'utilisation d'une classe est tout à fait justifié.
        #         """, task)

if correct_answers == 2:
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

compute_score(2, correct_answers)

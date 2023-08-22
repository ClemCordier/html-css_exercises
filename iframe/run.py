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
student_answer_q1 = input.get_input("document")
student_answer_q2 = input.get_input("youtube")
student_answer_q3 = input.get_input("map")

input.parse_template("template_q1.html")
input.parse_template("template_q2.html")
input.parse_template("template_q3.html")

raw_student_answers = {"document": [student_answer_q1, False], "youtube": [student_answer_q2, False], "map": [student_answer_q3, False]}

validation_errors_q1 = nu_checker_validation("template_q1.html", task="document", offset=7)
validation_errors_q2 = nu_checker_validation("template_q2.html", task="youtube", offset=7)
validation_errors_q3 = nu_checker_validation("template_q3.html", task="map", offset=7)

validation_errors = {"document": validation_errors_q1, "youtube": validation_errors_q2, "map": validation_errors_q3}
for task in validation_errors:
    if validation_errors[task]:
        raw_student_answers.pop(task)
        feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", task, True)
        for error in validation_errors[task]:
            feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : {error.get('message')}\n", task, True)

parsed_answers = parse_html_as_dict(raw_student_answers)

task_result = check_html_correctness(parsed_answers, expected_answers)

for task in task_result:
    if task_result.get(task):
        correct_answers += 1
        if task == "youtube":
            append_tip_feedback(
                """
                L'attribut booléen ``allowfullscreen`` permet d'obtenir le même résultat que ``allow: "fullscreen"``. Son utilisation est toutefois déconseillée (mais reste valide pour des raisons historiques).

                De même, l'attribut ``frameborder`` permettant de supprimer les bordures par défaut est *déprécié* (autrement dit, son utilisation est déconseillée par la spécification officielle).

                Ces attributs sont tout de même mentionnés à titre informatif. Bien que dépréciés, vous pourriez être amené à les croiser à l'avenir malgré tout. Cela peut donc s'avérer utile de savoir ce dont il retourne, même si vous ne vous en servez pas dans vos propres projets.

                Sur chaque page de documentation d'un élément HTML, `une section leur est dédiée <https://developer.mozilla.org/fr/docs/Web/HTML/Element/iframe#attributs_d%C3%A9pr%C3%A9ci%C3%A9s>`_.
                """, task
            )

compute_score(3, correct_answers)
if correct_answers == 3:
    append_tip_feedback(
        """
        Certains sites web proposent des éléments ``iframe`` pré-fait.

        C'est notamment le cas pour les vidéos *YouTube*, accessible via le bouton "Partager" sous le lecteur et en choisissant l'option "Intégrer" dans la fenêtre pop-up.
        """
    )
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

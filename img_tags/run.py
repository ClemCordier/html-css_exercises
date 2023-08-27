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
student_answer_q1 = input.get_input("path").strip()
student_answer_q2 = input.get_input("alt")


if student_answer_q1 == "../img/inginious_logo" or student_answer_q1 == "../img/inginious_logo.png":
    correct_answers += 1
    feedback.set_problem_result("success", "path")
    feedback.set_problem_feedback(
        """
        **Bonne réponse!**

        .. warning::
            :title: Attention

            **Bien que l'extension de fichier** (ici, ``.png``) **ne soit en théorie pas obligatoire pour que le chemin soit reconnu, nous tâcherons de le renseigner pour les questions qui suivent (ainsi que pour le restant du cours!)**
        """, "path", True)


    raw_student_answers = {"alt": [student_answer_q2, True]}

    validation_errors_q2 = is_invalid_self_closing_element(student_answer_q2)

    validation_errors = {"alt": validation_errors_q2}
    for task in validation_errors:
        if validation_errors[task]:
            raw_student_answers.pop(task) # removes non valid response
            feedback.set_problem_feedback(validation_errors[task], task, True) # append invalid fb msg

    parsed_answers = parse_html_as_dict(raw_student_answers)

    task_result = check_html_correctness(parsed_answers, expected_answers)

    for task in task_result:
        if task_result.get(task):
            correct_answers += 1
            if task == "alt":
                feedback.set_problem_feedback(
                    """
                    Voici ce qu'un utilisateur verrait en temps normal:
                    """, "alt", True
                )
                append_raw_html_feedback("""<img src="img_tags/inginious_logo.png" alt="Logo du site Inginious">""", task=task, title="Sans erreur:")
                deindented_fb = rst.indent_block(-2, "\n\nEt voici ce qu'un utilisateur verrait en cas de problème avec l'image:", "\t")
                feedback.set_problem_feedback(
                    deindented_fb, "alt", True
                )
                append_raw_html_feedback("""<img src="inginious_logo.png" alt="Logo du site Inginious">""", task=task, title="En cas d'erreur:")

                append_tip_feedback("""L'attribut ``alt``, bien que non obligatoire, mériterait d'être considéré comme tel. L'inclure de manière systématique lorsque vous insérez une image est une bonne pratique.

                Outre le fait de proposer une alternative à l'image, cet attribut est aussi lu par les lecteurs d'écran, facilitant la navigation aux personnes malvoyantes.""", "alt")

else:
    feedback.set_problem_result("failed", "path")
    feedback.set_problem_result("failed", "alt")
    feedback.set_problem_feedback("La réponse à la première question est incorrecte.", "alt", True)

if correct_answers == 2:
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

compute_score(2, correct_answers)
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
student_answer_q1 = input.get_input("label_input")
student_answer_q2 = input.get_input("label_input_for")
student_answer_q3 = input.get_input("input_password")
student_answer_q4 = input.get_input("input_attributes")

input.parse_template("template_q1.html")
input.parse_template("template_q2.html")
input.parse_template("template_q3.html")
input.parse_template("template_q4.html")

raw_student_answers = {"label_input": [student_answer_q1, False], "label_input_for": [student_answer_q2, False], "input_password": [student_answer_q3, False], "input_attributes": [student_answer_q4, False]}

validation_errors_q1 = nu_checker_validation("template_q1.html", offset=7)
validation_errors_q2 = nu_checker_validation("template_q2.html", offset=7)
validation_errors_q3 = nu_checker_validation("template_q3.html", offset=7)
validation_errors_q4 = nu_checker_validation("template_q4.html", offset=7)

validation_errors = {"label_input": validation_errors_q1, "label_input_for": validation_errors_q2, "input_password": validation_errors_q3, "input_attributes": validation_errors_q4}
for task in validation_errors:
    if validation_errors[task]:
        raw_student_answers.pop(task)
        feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", task, True)
        for error in validated_task[task]:
            feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : {error.get('message')}\n", task, True)

parsed_answers = parse_html_as_dict(raw_student_answers)

task_result = check_html_correctness(parsed_answers, expected_answers)

for task in task_result:
    if task_result.get(task):
        correct_answers += 1
        if task == "label_input":
            feedback.set_problem_feedback(
                """
                Grâce à cette information fournie au navigateur via l'attribut ``type="email"``, les appareils mobiles (tablette/téléphone) peuvent s'adapter en conséquence et proposer un layout de clavier avec la touche "@" par exemple.
                """, task, True
            )
        elif task == "label_input_for":
            feedback.set_problem_feedback(
                """
                Une façon alternative d'effectuer cette liaison est de changer **la relation** entre nos éléments: plutôt que d'avoir des éléments frères/soeurs (autrement dit, de même niveau dans la hiérarchie) nous allons utiliser l'élément ``label`` comme parent de notre élément de formulaire:

                .. code:: html

                    <label>Adresse mail:
                        <input type="email">
                    </label>

                .. tip::
                    :title: Tips

                    Nous favoriserons l'utilisation des attributs ``id`` et ``for`` dans le cadre de ce cours, mais il est toujours bon de connaître les notations alternatives afin d'être en mesure de comprendre le code d'une personne tierce !

                Cette liaison a plusieurs avantages:

                - Elle permet aux lecteurs d'écran de lire les libellés associés aux différents champs du formulaire, améliorant l'accessibilité aux personnes malvoyantes (tout comme l'attribut ``alt`` d'une image).
                - Elle permet un focus sur le champ du formulaire lors d'un clic souris (ou au toucher tactile pour un utilisateur tablette/téléphone) sur le libellé qui lui est associé.

                Essayez par vous-même ! Observez la différence avec l'exemple minimaliste fourni en introduction sans ces 2 attributs.
                """, task, True
            )
            append_raw_html_feedback(
                """
                <form>
                    <label for="email-input-q2">Adresse mail:</label>
                    <input id="email-input-q2" type="email">
                </form>
                """, task=task, title="Cliquez sur le libellé ci-dessous:")
        elif task == "input_password":
            feedback.set_problem_feedback(
                """
                Tapez des caractères dans le champ ci-dessous afin d'observer le comportement par défaut de la saisie de mot de passe.
                """, task, True
            )
            append_raw_html_feedback(
                """
                <form>
                    <label for="email-input-q3">Adresse mail:</label>
                    <input id="email-input-q3" type="email">
                    <label for="password-input-q3">Mot de passe:</label>
                    <input id="password-input-q3" type="password">
                </form>
                """, task=task, title="Saisissez du texte dans le champ de mot de passe:")



if correct_answers == 4:
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

compute_score(4, correct_answers)
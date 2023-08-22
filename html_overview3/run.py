#!/usr/bin/python3

import sys
sys.path.append("/course/common/utils")
from inginious_container_api import input, feedback, rst
from answer import expected_answer
from feedback_functions import *
from validation_functions import *
from parsing_functions import *
from correction_functions import *

input.parse_template("template.html")
answer = input.get_input("recipe")
correct_answers = 0
raw_student_answers = {"recipe": [answer, False]}

validation_errors = nu_checker_validation("template.html", task="recipe", offset=7)

if validation_errors:
    raw_student_answers.pop("recipe")
    feedback.set_problem_result("failed", "recipe")
    feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", "recipe", True)
    for error in validation_errors:
        feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : {error.get('message')}\n", "recipe", True)
else:
    parsed_student_answer = parse_html_as_dict(raw_student_answers)

    task_result = check_html_correctness(parsed_student_answer, expected_answer)
    for task in task_result:
        if task_result.get(task):
            correct_answers += 1
            append_raw_html_feedback(
                f"""
                <h1>Recette du jour - Tarte Tatin</h1>
                {answer.replace("images", "html_overview3")}
                <h2>Histoire</h2>
                ...
                """, task="recipe"
            )
            append_tip_feedback(
                """
                Quelques explications avancées sur le choix des éléments utilisés:

                - L'élément ``figure`` permet de créer une section propre à l'image, qui se détache du flux principal du document.
                - L'élément ``footer`` représente le pied de page **de l'élément sectionnant le plus proche** (généralement utilisé en bas de page d'un document, il représente ici le pied de page de l'élément ``figure``).
                - L'élément ``small`` est utilisé pour englober du texte correspondant à des copyrights, des mentions légales, etc. En outre, le style par défaut applique une taille de police plus petite à son contenu.
                """
            )

compute_score(1, correct_answers)
if correct_answers == 1:
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

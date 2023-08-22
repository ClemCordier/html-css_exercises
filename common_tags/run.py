#!/usr/bin/python3

# import re
import sys
sys.path.append("/course/common/utils")
from inginious_container_api import input, feedback, rst
from feedback_functions import *
from validation_functions import *
from parsing_functions import *
from correction_functions import *
from answer import expected_answer


student_answer_q1 = input.get_input("h1_tag").strip()
student_answer_q2 = input.get_input("p_tags")
input.parse_template("template.html")

correct_answers = 0

raw_student_answers = {"h1_tag": [student_answer_q1, True], "p_tags": [student_answer_q2, False]}

validation_errors_q1 = is_invalid_element(student_answer_q1)
validation_errors_q2 = nu_checker_validation("template.html", offset=7)

validation_errors = {"h1_tag": validation_errors_q1, "p_tags": validation_errors_q2}
for task in validation_errors:
    if validation_errors[task]:
        raw_student_answers.pop(task) # removes non valid response
        feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", task, True)
        if task == "h1_tag":
            feedback.set_problem_feedback(validation_errors[task], task, True) # append invalid fb msg

        if task == "p_tags":
            for error in validation_errors[task]:
                feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : {error.get('message')}\n", task, True)

if not validation_errors_q2:
    tag_errors_q2 = html_tags_validation(student_answer_q2)
    if tag_errors_q2:
        raw_student_answers.pop("p_tags")
        feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", "p_tags", True)
        for error in tag_errors_q2:
            feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : l'élément ``{error.get('element')}`` en position n°{error.get('element_number')} dans la hiérarchie ne semble pas être accompagné de sa balise fermante.\n", "p_tags", True)

parsed_student_answer = parse_html_as_dict(raw_student_answers)

task_result = check_html_correctness(parsed_student_answer, expected_answer)

for task in task_result:
    if task_result.get(task):
        correct_answers += 1
        if task == "h1_tag":
            append_tip_feedback(
                """
                L'élément ``h1`` est généralement utilisé une seule fois par document, pour le titre principal de votre page.
                """, task
            )
        elif task == "p_tags":
            append_tip_feedback(
                """
                Notez que les retours à la ligne dans le code au niveau du contenu d'un même élément (ici, ``p``) ne sont là que pour le confort du développeur.

                Ceux-ci ne se reflètent pas sur le rendu visible dans le navigateur (cf. feedback global).

                Nous verrons ultérieurement comment le langage interprète les espacements.
                """, task
            )


if correct_answers == 2:
    feedback.set_global_result("success")
    feedback.set_global_feedback(
        """
        Les 2 questions regroupées ensemble, voici ce que vous obtenez en ouvrant le document HTML dans un navigateur web:
        """
    )
    append_raw_html_feedback(
        """
        <h1>INGInious - Plateforme d'apprentissage informatique à destination des étudiants</h1>
        <p>
            La plateforme INGInious est créée et maintenue par le département d'ingénierie informatique de l'UCLouvain.
            Entièrement libre d'accès, son code-source est disponible sous licence open-source.
        </p>
        <p>
            Quand un étudiant soumet une réponse à un exercice de programmation, INGInious exécute automatiquement le programme écrit par l'étudiant et le soumet à une batterie de tests définis par l'enseignant.
            Grâce à ces tests, l'étudiant peut rapidement vérifier si sa réponse est correcte et sinon il corrige son programme jusqu'à ce qu'il réussisse les différents tests.
        </p>
        """
    )
    deindent = rst.indent_block(-2,
        """
        Vous remarquerez que le titre à un rendu bien différent de nos paragraphes.

        Ce rendu peut légèrement varier d'un navigateur à un autre, mais ce que l'on observe en règle général pour les éléments ``h1-h6``:

        - texte en gras
        - taille de police plus imposante (et qui décroît avec l'importance du titre choisi: un titre ``h1`` sera plus imposant qu'un titre ``h2``, qui sera lui-même plus imposant qu'un titre ``h3``, etc...)

        En réalité, **chaque élément HTML a un style par défaut qui lui est associé**. Nous pourrons modifier ce style comme bon nous semble à l'aide du langage CSS qui sera abordé dans la seconde partie de ce cours.

        Ne faites donc pas l'erreur d'utiliser des éléments HTML pour leur rendu visuel, **réservez-les plutôt pour leur sémantique !**
        """, "\t"
    )
    append_tip_feedback(deindent)

else:
    feedback.set_global_result("failed")

compute_score(2, correct_answers)

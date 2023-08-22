#!/usr/bin/python3

import sys
sys.path.append("/course/common/utils")
from inginious_container_api import input, feedback, rst
from feedback_functions import *
from validation_functions import *
from parsing_functions import *
from correction_functions import *
from answer import expected_answer


student_answer_q1 = input.get_input("reserved")
student_answer_q2 = input.get_input("symbol")
correct_answers = 0

raw_student_answers = {"reserved": [student_answer_q1, False], "symbol": [student_answer_q2, True]}

validation_errors_q1 = is_invalid_element(student_answer_q1)
validation_errors_q2 = is_invalid_element(student_answer_q2)

validation_errors = {"reserved": validation_errors_q1, "symbol": validation_errors_q2}
for task in validation_errors:
    if validation_errors[task]:
        raw_student_answers.pop(task) # removes non valid response
        feedback.set_problem_feedback(validation_errors[task], task, True) # append invalid fb msg


if student_answer_q1.strip().casefold() != "<p>la balise fermante d'un élément html est semblable à la balise ouvrante &lt;h1&gt; auquel on ajoute une barre oblique: &lt;/h1&gt;</p>":
    feedback.set_problem_result("failed", "reserved")
    raw_student_answers.pop("reserved")
    feedback.set_problem_feedback("Assurez-vous de répondre à l'aide des codes d'entités et non avec les symboles qu'ils représentent", "reserved", True)

if student_answer_q2.strip().casefold() != "<p>fourni par inginious v.x.x.x &copy; 2014-20xx université catholique de louvain.</p>":
    feedback.set_problem_result("failed", "symbol")
    raw_student_answers.pop("symbol")
    feedback.set_problem_feedback("Assurez-vous de répondre à l'aide du code d'entité et non avec le symbole qu'il représente", "symbol", True)

parsed_student_answer = parse_html_as_dict(raw_student_answers)


task_result = check_html_correctness(parsed_student_answer, expected_answer)

for task in task_result:
    if task_result.get(task):
        correct_answers += 1
        if task == "reserved":
            feedback.set_problem_result("success", task)
            feedback.set_problem_feedback(
                """
                Le problème avec l'exemple fourni est le suivant:

                Plutôt que d'être écrit telles quelles comme escompté, les balises ``<h1>`` et ``</h1>`` vont être interprétées en tant qu'élément HTML à part entière et non comme simple contenu.

                Voici le résultat (compromis) présent dans l'énoncé:
                """, task, True
            )

            append_raw_html_feedback(
                """
                <p>La balise fermante d'un élément html est semblable à la balise ouvrante <h1> auquel on ajoute une barre oblique: </h1></p>
                """, task=task, title="Sans entité:", is_file=False
            )

            deindent = rst.indent_block(-2,
                """
                \n\nEt voici le résultat (escompté) en se servant des entités:
                """, "\t"
            )
            feedback.set_problem_feedback(deindent, task, True)
            append_raw_html_feedback(
                """
                <p>La balise fermante d'un élément HTML est semblable à la balise ouvrante &lt;h1&gt; auquel on ajoute une barre oblique: &lt;/h1&gt;</p>
                """, task=task, title="Avec entité:", is_file=False
            )

        elif task == "symbol":
            feedback.set_problem_result("success", task)


compute_score(2, correct_answers)
if correct_answers == 2:
    feedback.set_global_feedback(
        """
        Vous retrouverez via le lien suivant une liste exhaustive des entités HTML: https://html.spec.whatwg.org/multipage/named-characters.html
        """, True
    )
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

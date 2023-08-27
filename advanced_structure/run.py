#!/usr/bin/python3

import sys
# import copy
sys.path.append("/course/common/utils")
from inginious_container_api import input, feedback, rst
from answer import expected_answers
from feedback_functions import *
from validation_functions import *
from parsing_functions import *
from correction_functions import *

correct_answers = 0
student_answer_q1 = input.get_input("header")
student_answer_q2 = input.get_input("main")
student_answer_q3 = input.get_input("footer")

raw_student_answers = {"header": [student_answer_q1, False], "main": [student_answer_q2, False], "footer": [student_answer_q3, False]}

validation_errors_q1 = nu_checker_validation("template_q1.html",task="header", offset=7)
validation_errors_q2 = nu_checker_validation("template_q2.html",task="main", offset=7)
validation_errors_q3 = nu_checker_validation("template_q3.html",task="footer", offset=7)

validation_errors = {"header": validation_errors_q1, "main": validation_errors_q2, "footer": validation_errors_q3}
for task in validation_errors:
    if validation_errors[task]:
        raw_student_answers.pop(task)
        feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", task, True)
        feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : {error.get('message')}\n", task, True)

parsed_student_answer = parse_html_as_dict(raw_student_answers)

task_result = check_html_correctness(parsed_student_answer, expected_answers)

for task in task_result:
    if task_result.get(task):
        correct_answers += 1


if correct_answers == 3:
    feedback.set_global_result("success")
    append_tip_feedback(
        """
        Vous aurez remarqué que nous avions déjà rencontré ``footer`` précédemment, inclus au sein de l'élément ``figure`` pour accompagner l'image de ses droits d'auteur.

        Ceci est un cas particulier, mais il n'en reste pas moins correct.

        Pour mieux le comprendre, voyons ce que nous dit la MDN pour les éléments `figure <https://developer.mozilla.org/fr/docs/Web/HTML/Element/figure>`_ et `footer <https://developer.mozilla.org/fr/docs/Web/HTML/Element/footer>`_ :

        .. raw:: html

            <ul>
                <li><em><code>figure</code> représente un contenu autonome [...] <code>figure</code> <strong>est une racine de sectionnement</strong>, son contenu est donc exclu du plan général du document.</em></li>
                <li><em><code>footer</code> représente le pied de page de la section <strong>ou de la racine de sectionnement la plus proche</strong>.</em></li>
            </ul>

        | Concrètement, cela implique que l'élément ``figure`` induit une section "à part entière", qui se distingue du plan global document.
        | Il est donc tout à fait envisageable de lui ajouter des éléments sectionnant (tel qu'un ``header`` ou un ``footer`` comme nous l'avons fait).
        """
    )
else:
    feedback.set_global_result("failed")

compute_score(3, correct_answers)
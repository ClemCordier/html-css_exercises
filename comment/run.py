#!/usr/bin/python3

import sys
sys.path.append("/course/common/utils")
from inginious_container_api import input, feedback, rst
from feedback_functions import *
from validation_functions import *
from parsing_functions import *
from correction_functions import *
from answer import expected_answer

input.parse_template("template.html") # for validation
answer_q1 = input.get_input("comment") # for parsing
correct_answers = 0

student_answer = {"comment": [answer_q1, False]}

validation_errors = nu_checker_validation("template.html")
if validation_errors:
    feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", "comment", True)
    for error in validation_errors:
        feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : {error.get('message')}\n", "comment", True)
else:
    parsed_student_answer = parse_html_as_dict(student_answer, skip_head=False, skip_comment=False)

    task_result = check_html_correctness(parsed_student_answer, expected_answer)
    for task in task_result:
        if task_result.get(task):
            correct_answers += 1
            append_tip_feedback(
                """
                Lorsqu'on ouvre un projet perso après l'avoir laissé de côté pendant un moment, il n'est pas rare de se demander pourquoi avoir écrit telle chose, avoir choisi telle option plutôt qu'une autre, ...

                Les commentaires peuvent vous servir d'aide-mémoire afin de justifier un choix d'implémentation, pour détailler un bout de code potentiellement complexe, ...

                En outre, les commentaires peuvent s'avérer très utile lorsque l'on travaille en collaboration sur un projet pour faciliter la compréhension de votre code à une personne tierce.
                """
            )
compute_score(1, correct_answers)
if correct_answers == 1:
    feedback.set_global_result("success")
else:
    feedback.set_global_result("failed")

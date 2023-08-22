#!/usr/bin/python3

import sys
# sys.path.append("/course/common")
sys.path.append("/course/common/utils")
from inginious_container_api import input, feedback, rst
from feedback_functions import *
from validation_functions import *
from parsing_functions import *
from correction_functions import *
from answer import expected_answer


input.parse_template("template.html") # for validation
answer_q1 = input.get_input("address") # for parsing

student_answer = {"address": [answer_q1, False]}

validation_errors = nu_checker_validation("template.html", offset=7)
if validation_errors:
    feedback.set_problem_feedback("Il y a des erreurs de syntaxe:\n\n", "address", True)
    for error in validation_errors:
        feedback.set_problem_feedback(f"- Ligne {error.get('line_number')} : {error.get('message')}\n", "address", True)
else:
    parsed_student_answer = parse_html_as_dict(student_answer)

    result = check_html_correctness(parsed_student_answer, expected_answer)
    if result["address"]:
        feedback.set_global_result("success")
        feedback.set_global_feedback(
            """
            +-------------------------------------------------------------+------------------------------------------------------------+
            |.. code:: html                                               |.. raw:: html                                               |
            |                                                             |                                                            |
            |    <address>                                                |    <address>                                               |
            |        Université catholique de Louvain                     |        Université catholique de Louvain                    |
            |        Department of Computing Science and Engineering      |        Department of Computing Science and Engineering     |
            |        Place Sainte-Barbe, 2 bte L5.02.01                   |        Place Sainte-Barbe, 2 bte L5.02.01                  |
            |        B-1348 Louvain-la-Neuve (Belgium)                    |        B-1348 Louvain-la-Neuve (Belgium)                   |
            |    </address>                                               |    </address>                                              |
            +-------------------------------------------------------------+------------------------------------------------------------+
            |.. code:: html                                               |.. raw:: html                                               |
            |                                                             |                                                            |
            |    <address>                                                |    <address>                                               |
            |        Université catholique de Louvain<br>                 |        Université catholique de Louvain<br>                |
            |        Department of Computing Science and Engineering<br>  |        Department of Computing Science and Engineering<br> |
            |        Place Sainte-Barbe, 2 bte L5.02.01<br>               |        Place Sainte-Barbe, 2 bte L5.02.01<br>              |
            |        B-1348 Louvain-la-Neuve (Belgium)                    |        B-1348 Louvain-la-Neuve (Belgium)                   |
            |    </address>                                               |    </address>                                              |
            +-------------------------------------------------------------+------------------------------------------------------------+
            """, True
        )
    else:
        feedback.set_global_result("failed")

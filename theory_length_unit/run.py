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
student_answer_q1 = input.get_input("px")
student_answer_q2 = input.get_input("em")
student_answer_q3 = input.get_input("rem")

input.parse_template("template_q1.css")
input.parse_template("template_q2.css")
input.parse_template("template_q3.css")

raw_student_answers = {"px": student_answer_q1, "em": student_answer_q2, "rem": student_answer_q3}

validation_errors_q1 = css_validator_validation("template_q1.css", task="px")
validation_errors_q2 = css_validator_validation("template_q2.css", task="em")
validation_errors_q3 = css_validator_validation("template_q3.css", task="rem")

validation_errors = {"px": validation_errors_q1, "em": validation_errors_q2, "rem": validation_errors_q3}

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
        if task == "px":
            append_tip_feedback(
                """
                Le pixel est l'unité de mesure la plus populaire de sa catégorie, et probablement la seule que vous devriez utiliser dans le cadre du développement web.

                Toutefois, il est à éviter pour du contenu textuel, comme tout autre unité de mesure **absolue**. Leur valeur est statique; elle ne s'adapte pas aux paramètres de l'utilisateur.

                +-------------------------------------------------------------------------------+
                | .. raw:: html                                                                 |
                |                                                                               |
                |     <img src="font_size/absolute_unit.gif" style="width: 100%; height:auto;"> |
                +-------------------------------------------------------------------------------+

                **Utiliser des pixels pour l'entièreté d'une page web, c'est donc inévitablement faire une croix sur son accessibilité.**
                """, task
            )
        if task == "em":
            append_tip_feedback(
                """
                Notez l'importance portée à "**à commencer par l'élément lui-même**".

                Si la propriété ``font-size`` d'un élément est explicitement redéfinie, alors toutes autres propriétés qui utilisent une unité de mesure relative sera calculée selon cette valeur.

                Pour illustrer cela, prenons la liste d'ingrédients de notre recette auquel la règle CSS ci-dessous est appliquée:

                .. code:: css

                    li {
                        font-size: 2.5em;
                        margin: 1em;
                    }

                +----------------------------------------------------------------------------+
                | .. raw:: html                                                              |
                |                                                                            |
                |   <img src="font_size/relative_unit.png" style="width: 20%; height:auto;"> |
                +----------------------------------------------------------------------------+

                La ``font-size`` est calculée sur base de l'élément racine (:math:`2.5*16px=40px`), tandis que les marges, elles, sont calculées sur base de l'élément ``li`` (donc :math:`1*40px` et non :math:`1*16px`)
                """, task
            )

if correct_answers == 3:
    append_tip_feedback(
        """
        Un solution (parmi d'autres) pour éviter d'être perdu par ce phénomène de composition lié au ``em``: utiliser uniquement des ``rem`` pour vos ``font-size`` afin d'avoir une base homogène.

        À partir de là, vous pouvez utiliser des ``em`` pour vos autres propriétés; leur valeur seront calculée sur cette même base.

        Le ``px`` est à réserver pour des éléments dont vous souhaitez expressément que ses dimensions soient fixe, indépendamment de tout le reste (ex: des bordures).
        """
    )
    feedback.set_global_result("success")

else:
    feedback.set_global_result("failed")

compute_score(3, correct_answers)
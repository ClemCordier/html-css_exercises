#!/usr/bin/python3

from html_elements import void_elements
from inginious_container_api import feedback, rst
from itertools import zip_longest
from copy import deepcopy
import difflib
import re


def check_mcq_correctness(student_answer, expected_answer, task, multiple_answer=False):
    if student_answer != expected_answer:
        feedback.set_problem_result("failed", task)
        feedback.set_problem_feedback(f"**Mauvaise réponse.**\n\n", task, True)
        if multiple_answer:
            wrong_choices = correct_choices = 0
            expected_choices = len(expected_answer)

            for choice in student_answer:
                if choice not in expected_answer:
                    wrong_choices += 1
                else:
                    correct_choices += 1
            feedback.set_problem_feedback(f"Il y a {wrong_choices} erreur(s) parmi votre réponse. Vous avez sélectionné {correct_choices}/{expected_choices} bonne(s) réponse(s).\n\n", task, True)
    else:
        feedback.set_problem_result("success", task)
        feedback.set_problem_feedback(f"**Bonne réponse!**\n\n", task, True)


def check_content_expectation(student_element, line, position, expected_element, task):
    words = student_element["element_text"].split()
    if student_element["element_name"].casefold() not in void_elements:
        if student_element["element_text"] != "" and expected_element["element_text"] != "":
            if len(words) > 30:
                provide_shortened_text = " ".join(words[:10]) + "\t(...)\t" + " ".join(words[-11:])
                feedback.set_problem_feedback(f"""-{line} Le contenu "*{provide_shortened_text}*" associé à l'élément ``{student_element["element_name"]}`` en position n°{position} dans la hiérarchie n'est pas celui attendu.\n""", task, True)
            else:
                feedback.set_problem_feedback(f"""-{line} Le contenu "*{student_element["element_text"]}*" associé à l'élément ``{student_element["element_name"]}`` en position n°{position} dans la hiérarchie n'est pas celui attendu.\n""", task, True)

        elif student_element["element_text"].casefold() == "" and expected_element["element_text"] != "":
            feedback.set_problem_feedback(f"""-{line} Le contenu de l'élément ``{student_element["element_name"]}`` en position n°{position} dans la hiérarchie est manquant.\n""", task, True)
        # * if the expected text SHOULD be empty but is not (such as html/head/body/ol/ul/... elements, cf. ignored_elements list in the parsing function)
        elif student_element["element_text"].casefold() != "" and expected_element["element_text"] == "":
            feedback.set_problem_feedback(f"""-{line} L'élément ``{student_element["element_name"]}`` en position n°{position} dans la hiérarchie n'attend pas de contenu.\n""", task, True)
    else:
        if len(expected_element["element_text"]) > 0:
            if not len(student_element["element_text"]) > 0 or not (
                (
                    len(student_element["element_text"]) > len(expected_element["element_text"])
                    and student_element["element_text"][:len(expected_element["element_text"])].casefold() == expected_element["element_text"]
                )
                or
                (
                    len(student_element["element_text"]) < len(expected_element["element_text"])
                    and student_element["element_text"].casefold() == expected_element["element_text"][:len(student_element["element_text"])]
                )
            ):
                feedback.set_problem_feedback(f"""-{line} L'élément vide ``{student_element["element_name"]}`` en position n°{position} dans la hiérarchie ne semble pas être renseigné au bon endroit.\n""", task, True)


def check_html_correctness(student_answers, expected_answers):
    """Compare student answers (task by task) to the hard-coded expected ones

    :param student_answers: the parsed HTML code submitted by the student
    :type student_answers: dict
    :param expected_answers: contains the following key-value pair: {task_id: expected_answer} that represents the expected code structure for each task
    :type expected_answers: dict
    :returns: task_result, contains the following key-value pair: {task_id: True/False} that indicates whether a task has correctly been answered
    :rtype: dict
    """

    task_result = {}
    task_line = {}
    normalized_student_answers = {}
    correct_elements = {}
    for task in student_answers:
        task_result[task] = False
        task_line[task] = deepcopy(student_answers[task].pop()) # * is deepcopy necessary here ? if so, can't remember why
        normalized_student_answers[task] = []
        correct_elements[task] = []
        error_found = False
        # * NORMALIZE AND RETRIEVE EVERY EXPECTED ELEMENT FROM STUDENT ANSWER, UP TO THE FIRST ENCOUNTERED ERROR
        for student_element, expected_element in zip_longest(student_answers[task],expected_answers[task]):
            if expected_element is None or student_element is None:
                error_found = True
            if student_element is not None:
                normalized_student_element = {}
                normalized_attr = {}
                normalized_student_element["element_name"] = student_element["element_name"].casefold()
                for attr in student_element["element_attr"]:
                    normalized_attr[attr.casefold()] = student_element["element_attr"][attr].casefold()
                normalized_student_element["element_attr"] = normalized_attr
                normalized_student_element["element_text"] = student_element["element_text"].casefold()
                normalized_student_answers[task].append(normalized_student_element)

                if expected_element is None:
                    continue

                attr_expectation_check = [attr in expected_element["element_attr"] for attr in normalized_attr]
                attr_value_check = [(
                    (not isinstance(expected_element["element_attr"][attr], set) and normalized_student_element["element_attr"][attr] == expected_element["element_attr"][attr])
                    or
                    (isinstance(expected_element["element_attr"][attr], set) and normalized_student_element["element_attr"][attr] in expected_element["element_attr"][attr])
                ) for attr in normalized_attr if attr in expected_element["element_attr"]]

                if (
                    (not error_found)
                    and
                    (
                        (normalized_student_element["element_name"] == expected_element["element_name"] and len(student_element["element_attr"]) == len(expected_element["element_attr"]) and all(attr_expectation_check) and all(attr_value_check))
                        and
                        (
                            (normalized_student_element["element_text"] == expected_element["element_text"])
                            or
                            (
                                normalized_student_element["element_name"] in void_elements and len(normalized_student_element["element_text"]) > 0
                                and
                                (
                                    (
                                        len(student_element["element_text"]) > len(expected_element["element_text"])
                                        and normalized_student_element["element_text"][:len(expected_element["element_text"])] == expected_element["element_text"]
                                    )
                                    or
                                    (
                                        len(student_element["element_text"]) < len(expected_element["element_text"])
                                        and normalized_student_element["element_text"] == expected_element["element_text"][:len(student_element["element_text"])]
                                    )
                                )
                            )
                        )
                    )
                ):
                    correct_elements[task].append(f"""``{normalized_student_element["element_name"]}``""")
                else:
                    error_found = True


        if normalized_student_answers[task] != expected_answers[task] and error_found:
            feedback.set_problem_result("failed", task)
            feedback.set_problem_feedback("Voici des pistes qui pourraient vous aider:\n\n", task, True)

            # * return the n-th first correct element (up to the first encountered error) as feedback to the student
            first_error_pos = len(correct_elements[task])
            if first_error_pos == 1:
                feedback.set_problem_feedback(f"""- Le premier élément ({correct_elements[task][0]}) est correct.\n""", task, True)
            elif first_error_pos > 1:
                feedback.set_problem_feedback(f"""- Les {first_error_pos} premiers éléments ({" , ".join(correct_elements[task])}) sont corrects.\n""", task, True)

            # * IF NB OF STUDENT ELEMENTS != NB OF EXPECTED ELEMENTS
            if len(student_answers[task]) != len(expected_answers[task]):
                feedback.set_problem_feedback(f"- Vous n'avez pas renseigné le bon nombre d'éléments: attendu {len(expected_answers[task])} - reçu {len(student_answers[task])}\n", task, True)

                for element_position, (student_element, line_number, expected_element) in enumerate(zip_longest(normalized_student_answers[task][first_error_pos:], task_line[task][first_error_pos:], expected_answers[task][first_error_pos:]), first_error_pos+1):
                    provide_line_number = ""
                    provide_element_position = ""
                    if line_number != None and len(set(task_line[task])) > 1:
                        provide_line_number = f" Ligne {line_number}:"
                    if len(normalized_student_answers[task]) > 1:
                        provide_element_position = f" en position n°{element_position} dans la hiérarchie"
                    if student_element is not None and expected_element is not None:
                        if student_element["element_name"] != expected_element["element_name"]:
                            feedback.set_problem_feedback(f"""-{provide_line_number} L'élément ``{student_element["element_name"]}`` ne correspond pas à l'élément attendu{provide_element_position}.\n""", task, True)
                        else:
                            if student_element["element_text"] != expected_element["element_text"]:
                                check_content_expectation(student_element, provide_line_number, element_position, expected_element, task)
                            if student_element["element_attr"] != expected_element["element_attr"]:
                                if len(student_element["element_attr"]) != len(expected_element["element_attr"]):
                                    feedback.set_problem_feedback(f"""-{provide_line_number} Vous n'avez pas renseigné le bon nombre d'attributs à l'élément ``{student_element["element_name"]}``{provide_element_position}: attendu {len(expected_element["element_attr"])} - reçu {len(student_element["element_attr"])}\n\n""", task, True)
                                else:
                                    feedback.set_problem_feedback(f"""-{provide_line_number} Le(s) attribut(s) associé(s) à l'élément ``{student_element["element_name"]}``{provide_element_position} contiennent des erreurs:\n\n""", task, True)
                                for attr in student_element["element_attr"]:
                                    if not attr.casefold() in expected_element["element_attr"]:
                                        feedback.set_problem_feedback(rst.indent_block(1, f"""- L'attribut ``{attr}`` associé à l'élément ``{student_element["element_name"]}`` ne fait pas partie du/des attribut(s) attendu(s).\n""", "\t"), task, True)
                                    elif (not isinstance(expected_element["element_attr"][attr], set) and student_element["element_attr"][attr] != expected_element["element_attr"][attr]) or (isinstance(expected_element["element_attr"][attr], set) and student_element["element_attr"][attr] not in expected_element["element_attr"][attr]):
                                        feedback.set_problem_feedback(rst.indent_block(1, f"""- La valeur "*{student_element["element_attr"][attr]}*" assignée à l'attribut ``{attr}`` n'est pas celle attendue.\n""", "\t"), task, True)
                    else:
                        break

            # * IF NB OF STUDENT ELEMENTS == NB OF EXPECTED ELEMENTS
            else:
                for element_position, (student_element, normalized_student_element, line_number, expected_element) in enumerate(zip(student_answers[task][first_error_pos:], normalized_student_answers[task][first_error_pos:], task_line[task][first_error_pos:], expected_answers[task][first_error_pos:]), first_error_pos+1):

                    provide_line_number = ""
                    provide_element_position = ""
                    if line_number != None and len(set(task_line[task])) > 1:
                        provide_line_number = f" Ligne {line_number}:"
                    if len(normalized_student_answers[task]) > 1:
                        provide_element_position = f" en position n°{element_position} dans la hiérarchie"

                    if normalized_student_element != expected_element:
                        if normalized_student_element["element_name"] != expected_element["element_name"]:
                            feedback.set_problem_feedback(f"""-{provide_line_number} L'élément ``{student_element["element_name"]}`` ne correspond pas à l'élément attendu{provide_element_position}.\n""", task, True)
                        else:
                            if normalized_student_element["element_text"] != expected_element["element_text"]:
                                check_content_expectation(student_element, provide_line_number, element_position, expected_element, task)
                            if normalized_student_element["element_attr"] != expected_element["element_attr"]:
                                if len(student_element["element_attr"]) != len(expected_element["element_attr"]):
                                    feedback.set_problem_feedback(f"""-{provide_line_number} Vous n'avez pas renseigné le bon nombre d'attributs à l'élément ``{student_element["element_name"]}``{provide_element_position}: attendu {len(expected_element["element_attr"])} - reçu {len(student_element["element_attr"])}\n\n""", task, True)
                                else:
                                    feedback.set_problem_feedback(f"""-{provide_line_number} Le(s) attribut(s) associé(s) à l'élément ``{student_element["element_name"]}``{provide_element_position} contiennent des erreurs:\n\n""", task, True)
                                for attr in student_element["element_attr"]:
                                    if not attr.casefold() in expected_element["element_attr"]:
                                        feedback.set_problem_feedback(rst.indent_block(1, f"""- L'attribut ``{attr}`` associé à l'élément ``{student_element["element_name"]}`` ne fait pas partie du/des attribut(s) attendu(s).\n""", "\t"), task, True)
                                    elif (not isinstance(expected_element["element_attr"][attr], set) and normalized_student_element["element_attr"][attr] != expected_element["element_attr"][attr]) or (isinstance(expected_element["element_attr"][attr], set) and student_element["element_attr"][attr] not in expected_element["element_attr"][attr]):
                                        feedback.set_problem_feedback(rst.indent_block(1, f"""- La valeur "*{student_element["element_attr"][attr]}*" assignée à l'attribut ``{attr}`` n'est pas celle attendue.\n""", "\t"), task, True)

        else:
            feedback.set_problem_result("success", task)
            feedback.set_problem_feedback("**Correct !**\n\n", task, True)
            task_result[task] = True

    return task_result


def check_css_correctness(student_answers, expected_answers, check_line=True):
    """Compare student answers (task by task) to the hard-coded expected ones

    :param student_answers: the parsed CSS code submitted by the student
    :type student_answers: dict
    :param expected_answers: contains the following key-value pair: {task_id: expected_answer} that represents the expected code structure for each task
    :type expected_answers: dict
    :returns: task_result, contains the following key-value pair: {task_id: True/False} that indicates whether a task has correctly been answered
    :rtype: dict
    """

    task_result = {}
    task_line = {}
    for task in student_answers:
        task_result[task] = False
        if check_line:
            task_line = deepcopy(student_answers[task].pop())
        else:
            task_line = dict.fromkeys(student_answers.keys(), [0 for _ in range(len(student_answers[task]))])


    if student_answers != expected_answers:
        for task in student_answers:
            if student_answers[task] != expected_answers[task]:
                is_incorrect = False
                feedback.set_problem_result("failed", task)
                if student_answers[task] == []:
                    continue
                elif len(student_answers[task]) != len(expected_answers[task]):
                    is_incorrect = True
                    feedback.set_problem_feedback("Voici des pistes qui pourraient vous aider:\n\n", task, True)
                    feedback.set_problem_feedback(f"- Vous n'avez pas renseigné le bon nombre de règles: attendu {len(expected_answers[task])} - reçu {len(student_answers[task])}\n", task, True)
                else:
                    rule_pos = 0
                    correct_selec = []
                    expected_selec = []
                    for rule in expected_answers[task]:
                        expected_selec.append(rule[0])

                    for rule, student_rule, line_info in zip(expected_answers[task], student_answers[task], task_line[task]):
                        selec = rule[0]
                        student_selec = student_rule[0]
                        properties = rule[1]
                        student_properties = student_rule[1]
                        rule_pos += 1

                        provide_line_info = "" if not check_line else f" Ligne {line_info[student_selec]}:"
                        # * check selector correctness
                        if (not isinstance(selec, set) and student_selec != selec) or (isinstance(selec, set) and student_selec not in selec):
                            feedback.set_problem_feedback(f"-{provide_line_info} Le sélecteur ``{student_selec}`` n'est pas celui attendu.\n", task, True)
                            # * prevent checking for declarations if the selector is already in fault
                            continue

                        # * check # of properties
                        elif len(properties) != len(student_properties):
                            feedback.set_problem_feedback(f"- Vous n'avez pas renseigné le bon nombre de propriétés au sélecteur ``{selec}``: attendu {len(properties)} - reçu {len(student_properties) }\n\n", task, True)

                        # * RETURN DETAILED INFO ABOUT PROPERTIES EXPECTATION AS FEEDBACK TO THE STUDENT
                        correct_properties = set()
                        for (prop_name, prop_value), (student_prop_name, student_prop_value) in zip_longest(properties.items(), student_properties.items(), fillvalue=(None, None)):

                            # * retrieve unexpected properties from student answer
                            if student_prop_name not in list(properties.keys()) and student_prop_name is not None:
                                provide_line_info = "" if not check_line else f" Ligne {line_info[student_prop_name]}:"
                                feedback.set_problem_feedback(f"-{provide_line_info} Êtes-vous sûr d'avoir besoin de la propriété ``{student_prop_name}`` afin de répondre à cette question ?\n", task, True)

                            # * retrieve missing properties from student answer
                            if prop_name not in list(student_properties.keys()) and prop_name is not None:
                                feedback.set_problem_feedback(f"- La propriété suivante est manquante: ``{prop_name}``\n", task, True)


                            if student_prop_name in list(properties.keys()):
                                if (not isinstance(properties[student_prop_name], set) and student_prop_value.casefold() != properties[student_prop_name]) or (isinstance(properties[student_prop_name], set) and student_prop_value.casefold() not in properties[student_prop_name]):
                                    provide_line_info = "" if not check_line else f" Ligne {line_info[student_prop_name]}:"
                                    feedback.set_problem_feedback(f"-{provide_line_info} La valeur ``{student_prop_value}`` associée à la propriété ``{student_prop_name}`` est incorrecte.\n", task, True)
                                else:
                                    correct_properties.add(student_prop_name)

                        if len(correct_properties) == len(list(properties.keys())) and len(correct_properties) == len(list(student_properties.keys())):
                            correct_selec.append(student_selec)

                    for received, expected in zip_longest(correct_selec, expected_selec):
                        if (isinstance(expected, set) and received not in expected) or (not isinstance(expected, set) and received != expected):
                            is_incorrect = True

                if not is_incorrect:
                    feedback.set_problem_result("success", task)
                    feedback.set_problem_feedback("**Correct !**\n\n", task, True)
                    task_result[task] = True
                    continue

            else:
                feedback.set_problem_result("success", task)
                feedback.set_problem_feedback("**Correct !**\n\n", task, True)
                task_result[task] = True

        return task_result

    for task in task_result:
        feedback.set_problem_result("success", task)
        feedback.set_problem_feedback("**Correct !**\n\n", task, True)
        task_result[task] = True

    feedback.set_global_result("success")
    return task_result


if __name__ == "__main__":
    pass

#!/usr/bin/python3

from inginious_container_api import feedback
import re
import cssutils, tinycss2
import lxml.html as lxml_html
from html_elements import ignored_elements_content, head_elements


def parse_html_as_dict(tasks, skip_head=True, skip_comment=True):
    """Parse the HTML code submitted by the student task by task and create a dictionary-based structure out of it.

    :param tasks: {task_id1: [student_answer_q1, is_single_element], task_id2: [student_answer_q2, is_single_element], ...}
    :type tasks: dict
    :param skip_head: whether or not head element (child(ren) included) must be ignored
    :type skip_head: bool
    :param skip_comment: whether or not comments must be ignored
    :type skip_comment: bool
    :returns: student_answers =
            {
                task_id1: [
                        {'element_name': element_name1, 'element_attr': {attr_name1: attr_value1, attr_name2: attr_value2}, 'element_text': element_text},
                        {'element_name': element_name2, 'element_attr': {attr_name: attr_value}, 'element_text': element_text},
                        ...
                    ],
                task_id2: [
                        {'element_name': element_name1, 'element_attr': {attr_name1: attr_value1, attr_name2: attr_value2}, 'element_text': element_text},
                        ...
                    ],
                    ...
            }
    :rtype: dict
    """

    pattern = r'(\s+)' # pattern necessary to normalize spacing in order to prevent issue with content
    student_answers = {}
    for task_id, task in tasks.items():
        student_answers[task_id] = []
        element_line = []
        is_single_element = task.pop()
        task_answer = task.pop()
        offset = task.pop() if task else 0
        if is_single_element:
            try:
                element = lxml_html.fragment_fromstring(task_answer, base_url=None, parser=None)
            except:
                feedback.set_problem_feedback(f"Une erreur est survenue lors de l'analyse syntaxique.\n\n", task_id, True)

            elem_data = {"element_name": element.tag, "element_attr": element.attrib, "element_text": re.sub(pattern, " ", element.text_content()).strip()}
            student_answers[task_id].append(elem_data)
            element_line.append(element.sourceline - offset)

        else:
            try:
                elements = lxml_html.document_fromstring(task_answer, parser=None)
            except:
                feedback.set_problem_feedback(f"Une erreur est survenue lors de l'analyse syntaxique.\n\n", task_id, True)

            for element in elements.iter():
                # * early check to prevent useless computation if element must be skipped (e.g. elements from template or comments)
                if (skip_head and isinstance(element, lxml_html.HtmlElement) and (element.tag in head_elements or element.tag == 'html' or element.tag == 'body')) or (skip_comment and isinstance(element, lxml_html.HtmlComment)):
                    continue

                retrieve_content = retrieve_element_content(element)
                elem_content = "".join(retrieve_content)

                # * check whether it's an actual element or a comment
                if isinstance(element, lxml_html.HtmlElement):
                    elem_data = {"element_name": element.tag, "element_attr": element.attrib, "element_text": re.sub(pattern, " ", elem_content).strip()}
                elif isinstance(element, lxml_html.HtmlComment):
                    elem_data = {"element_name": "comment", "element_attr": {}, "element_text": re.sub(pattern, " ", elem_content).strip()}

                student_answers[task_id].append(elem_data)
                element_line.append(element.sourceline - offset)
        student_answers[task_id].append(element_line)

    return student_answers

def retrieve_element_content(element):
    """Retrieve element content, children content included (except for a given set of element, cf. ignored_element_content)

    :param element: the current element
    :type element: lxml obj
    :returns: the content for the current element
    :rtype: str
    """

    content = []

    # * retrieve element content, if it exists
    if element.text is not None:
        content.append(element.text)
    # * elif element has no content (such as void elements), retrieve its tail content instead (i.e. the text that comes just after the element, up to the next encountered element)
    elif element.tail is not None:
        content.append(element.tail)

    # * recursively iterate on child(ren) element(s)
    if element.tag not in ignored_elements_content:
        for child_element in element.iterchildren():
            child_content = retrieve_element_content(child_element)
            content.extend(child_content)
            # * if the child is not a void element, retrieve both its content and its tail content
            if child_element.text is not None and child_element.tail is not None:
                content.append(child_element.tail)

    return content


def get_specificity(selector_list):
    specificities = {}
    for selector in selector_list:
        specificities[selector.selectorText] = selector.specificity
    return specificities


def sort_lines(data, order_structure):
    order_mapping = {list(item.keys())[0]: list(item.values())[0] for item in order_structure}
    sorted_data = sorted(data, key=lambda item: custom_sort_key1(item, order_mapping))
    return sorted_data

def custom_sort_key1(item, order_mapping):
    key = list(item.keys())[0]
    return order_mapping[key]

def sort_rules(data, order_structure):
    order_mapping = {item[0]: list(order.values())[0] for item, order in zip(data, order_structure)}
    sorted_data = sorted(data, key=lambda item: custom_sort_key2(item, order_mapping))
    return sorted_data

def custom_sort_key2(item, order_mapping):
    key = item[0]
    return order_mapping[key]


def parse_css_as_dict(tasks, skip_comments=True, skip_whitespace=True, debug=False):
    """Parse the CSS code submitted by the student task by task and create a dictionary-based structure out of it.

    :param tasks: {task_id1: student_answer_q1, task_id2: student_answer_q2, ...}
    :type tasks: dict
    :param skip_comments: whether or not comments must be ignored
    :type skip_comments: bool
    :param skip_whitespace: whether or not spaces must be ignored
    :type tasks: bool
    :returns: student_answers =
            {
                task_id1:
                    [
                        (selector_block1, {property1: {accepted_value1, accepted_value2} , property2: value2}),
                        (selector_block2, {property1: value1, ...}, ...),
                        ...
                    ],
                task_id2:
                    [
                        (selector_block1, {property1: value1 , property2: value2}),
                        ...
                    ],
                ...
            }
    :rtype: dict
    """

    student_answers = {}
    sorted_student_answers = {}
    task_line = {}
    for task_id, task_answer in tasks.items():
        student_answers[task_id] = []
        task_line[task_id] = []
        sorted_student_answers[task_id] = None
        try:
            sheet = tinycss2.parse_stylesheet(task_answer, skip_comments=skip_comments, skip_whitespace=skip_whitespace)
            css = cssutils.parseString(task_answer)
        except:
            feedback.set_problem_feedback(f"Une erreur est survenue lors de l'analyse syntaxique.\n\n", task_id, True)
        rules = []
        for tiny_rule, utils_rule in zip(sheet, css.cssRules):
            specs = get_specificity(utils_rule.selectorList)
            for sel, spec in specs.items():
                rules.append({sel: spec})

        for idx, rule in enumerate(sheet):
            rule_line = {}
            if rule.type == "qualified-rule":
                is_composed = False
                previous_token = None
                for token in rule.prelude:
                    if token.value == ".":
                        previous_token = token.value
                        is_composed = True
                        continue
                    elif token.value == "*":
                        selector = token.value
                    elif token.type != "hash" and token.type != "ident":
                        continue
                    elif token.type == "hash":
                        selector = "#"+token.value
                    elif token.type == "ident":
                        selector = previous_token+token.lower_value if is_composed else token.lower_value
                    is_composed = False
                    rule_line[selector] = rule.source_line
                    properties = {}
                    for declaration in tinycss2.parse_declaration_list(rule.content):
                        if declaration.type == "declaration":
                            rule_line[declaration.name.strip().casefold()] = declaration.source_line
                            properties[declaration.name.strip().casefold()] = tinycss2.serialize(declaration.value).strip()
                    student_answers[task_id].append((selector, properties))
                    task_line[task_id].append({selector: rule_line})

        sorted_lines = sort_lines(task_line[task_id], rules)
        task_line[task_id] = [list(inner_dict.values())[0] for inner_dict in sorted_lines]
        sorted_rules = sort_rules(student_answers[task_id], rules)
        task_line[task_id] = [list(inner_dict.values())[0] for inner_dict in sorted_lines]
        sorted_student_answers[task_id] = sorted_rules
        sorted_student_answers[task_id].append(task_line)
    return sorted_student_answers



def parse_inline_css_as_dict(tasks):
    student_answers = {}
    for task_id, task_answer in tasks.items():
        student_answers[task_id] = []
        try:
            element = lxml_html.fragment_fromstring(task_answer)
        except:
            feedback.set_problem_feedback(f"Une erreur est survenue lors de l'analyse syntaxique.\n\n", task_id, True)

        style_attr = element.get('style')
        if style_attr is None:
            feedback.set_problem_feedback(f"Assurez-vous d'utiliser l'attribut ``style`` pour répondre à cette question.\n\n", task_id, True)
            continue
        try:
            style = tinycss2.parse_declaration_list(style_attr)
        except:
            feedback.set_problem_feedback(f"Une erreur est survenue lors de l'analyse syntaxique.\n\n", task_id, True)
        properties = {}
        for decl in style:
            try:
                properties[decl.name.casefold()] = tinycss2.serialize(decl.value).strip().casefold()
            except:
                feedback.set_problem_feedback(f"Une erreur est survenue lors de l'analyse syntaxique.\n\n", task_id, True)
            student_answers[task_id] = [(element.tag, properties)]

    return student_answers


if __name__ == "__main__":
    pass

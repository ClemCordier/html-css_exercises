#!/usr/bin/python3


from inginious_container_api import feedback
import shlex, subprocess, json
import re
import operator
from html_elements import existing_elements, void_elements


def is_invalid_opening_tag(tag):
    """Take a single opening tag as input and compare it against a regular expression to ensure its syntax is valid

    :param tag: The opening tag
    :type tag: str
    :return: None if the provided tag is considered valid and match an existing element, generic error messages if the tag is invalid or unrecognized
    :rtype: str
    """

    match = re.fullmatch(r"<([a-z]+[0-9]?)(\s{1}[a-z\-_]+(\s?=\s?(?:\".*?\"|'.*?'|[^'\">\s]+))?)*>", tag)
    if match:
        if match.group(1) in existing_elements:
            return None
        else:
            return f"""
                   L'élément {match.group(1)} renseigné ne semble pas correspondre à un élément HTML existant.
                   """
    return  f"""
            Votre réponse ``{tag.strip()}`` ne semble pas correspondre à une balise ouvrante valide.

            Assurez-vous de respecter la syntaxe de base ainsi que l'écriture conventionnelle d'une balise ouvrante, c'est-à-dire:

            - nom de la balise en minuscule.
            - pas d'espacement au sein de votre balise, sauf pour y ajouter des attributs (voire entre l'attribut et sa valeur).

            | exemple: ``<div>``, ``<div attribut="valeur" attribut="valeur">``, ``<div attribut = 'valeur'>``
            | contre-exemple: ``<DIV>``, ``<div attribut=" valeur ">``, ``<div attribut=valeur>``
            |

            N'hésitez pas à consulter la `section théorique <https://inginious.org/course/html_css_clement/theory_html_basics>`_ en cas de doute.
            """

def is_invalid_closing_tag(tag):
    """Take a single closing tag as input and compare it against a regular expression to ensure its syntax is valid

    :param tag: The closing tag
    :type tag: str
    :return: None if the provided tag is considered valid and match an existing element, generic error messages if the tag is invalid or unrecognized
    :rtype: str
    """

    match = re.fullmatch(r"</([a-z]+[0-9]?)>", tag)
    if match:
        if match.group(1) in existing_elements:
            return None
        else:
            return f"""
                   L'élément {match.group(1)} renseigné ne semble pas correspondre à un élément HTML existant.
                   """
    return  f"""
            Votre réponse ``{tag.strip()}`` ne semble pas correspondre à une balise fermante valide.

            Assurez-vous de respecter la syntaxe de base ainsi que l'écriture conventionnelle d'une balise fermante, c'est-à-dire:

            - nom de la balise en minuscule.
            - pas d'espacement au sein de votre balise.

            | exemple: ``</div>``
            | contre-exemple: ``< /div>``, ``</DIV>``, ``</div >``
            |

            N'hésitez pas à consulter la `section théorique <https://inginious.org/course/html_css_clement/theory_html_basics>`_ en cas de doute.
            """

def is_invalid_self_closing_element(element):
    """Take a self-closing element as input and compare it against a regular expression to ensure its syntax is valid

    :param element: The self-closing element
    :type element: str
    :return: None if the provided element is considered valid and match an existing element, generic error messages if the element is invalid or unrecognized
    :rtype: str
    """

    match = re.fullmatch(r"<([a-z]+[0-9]?)(\s{1}[a-z\-_]+(\s?=\s?(?:\".*?\"|'.*?'|[^'\">\s]+))?)*\s?\/?>", ' '.join(element.split()))
    if match:
        if match.group(1) in existing_elements:
            return None
        else:
            return f"""
                   L'élément ``{match.group(1)}`` renseigné ne semble pas correspondre à un élément HTML existant.
                   """
    return  f"""
            Votre réponse ``{element.strip()}`` ne semble pas correspondre à un élément vide valide.

            Assurez-vous de respecter la syntaxe de base ainsi que l'écriture conventionnelle d'un élément vide, c'est-à-dire:

            - nom de la balise (et des éventuels atrributs) en minuscule.
            - pas d'espacement au sein de votre balise, sauf pour y ajouter des attributs (voire entre l'attribut et sa valeur) ou avant la fermeture de la balise si vous optez pour l'écriture avec barre oblique (/>).

            | exemple: ``<img src="image.png" />``, ``<img src = "image.png">``
            | contre-exemple: ``<img src="image.png"  >`` (remarquez l'espacement avant le caractère de fermeture ``>``)
            |

            N'hésitez pas à consulter la `section théorique <https://inginious.org/course/html_css_clement/theory_html_basics>`_ en cas de doute.
            """

def is_invalid_element(element):
    """Take a (non self-closing) element as input and compare it against a regular expression to ensure its syntax is valid

    :param element: The element
    :type element: str
    :return: None if the provided element is considered valid and match an existing element, generic error messages if the element is invalid or unrecognized
    :rtype: str
    """

    match = re.fullmatch(r"<([a-z]+[0-9]?)(\s{1}[a-z\-_]+(\s?=\s?(?:\".*?\"|'.*?'|[^'\">\s]+))?)*>[^><]*<\/\1>", element)
    if match:
        if match.group(1) in existing_elements:
            return None
        else:
            return f"""
                   L'élément ``{match.group(1)}`` renseigné ne semble pas correspondre à un élément HTML existant.
                   """
    return  f"""
            Votre réponse ``{element.strip()}`` ne semble pas correspondre à un élément HTML valide.

            Assurez-vous de respecter la syntaxe de base ainsi que l'écriture conventionnelle d'un élément, c'est-à-dire:

            - nom des balises (et des éventuels atrributs) en minuscule.
            - pas d'espacement au sein de votre balise ouvrante, sauf pour y ajouter des attributs (voire entre l'attribut et sa valeur).
            - pas d'espacement au sein de votre balise fermante.

            | exemple: ``<p id="premier-paragraphe">contenu du paragraphe</p>``
            | contre-exemple: ``<P id="premier-paragraphe">contenu du paragraphe</P>``, ``<p id="premier-paragraphe">contenu du paragraphe<   /p   >`` (remarquez l'espacement au sein de la balise fermante), ...
            |

            N'hésitez pas à consulter la `section théorique <https://inginious.org/course/html_css_clement/theory_html_basics>`_ en cas de doute.
            """


def html_tags_validation(html_code):
    stack = []
    lines = html_code.split('\n')
    stripped_lines = [line.strip() for line in lines]
    elem_number = 0
    for line_number, line in enumerate(stripped_lines, start=1):
        matched_tags = []
        for match in re.finditer(r"(<\/?\w+(\s{1}[\w-]+(\s?=\s?(?:\".*?\"|'.*?'|[^'\">\s]+))?)*\s*\/?>)", line):
            matched_tags.append(match.group(1))
        if matched_tags:
            for tag in matched_tags:
                if '</' in tag:
                    element_to_pop = tag[2:len(tag)-1].replace(' ', '')
                    for idx, tag in reversed(list(enumerate(stack))):
                        if tag['element'] == element_to_pop:
                            stack.pop(idx)
                            if element_to_pop != 'html':
                                break
                else:
                    elem_number += 1
                    tag_obj = {'tag': tag, 'line_number': line_number, 'element_number': elem_number}
                    if ' ' in tag:
                        tag_obj['element'] = tag[1:tag.index(' ')]
                    elif '/' in tag:
                        tag_obj['element'] = tag[1:tag.index('/')]
                    else:
                        tag_obj['element'] = tag[1:len(tag) - 1]
                    is_self_closing = tag_obj['element'].casefold() in void_elements
                    if not is_self_closing:
                        stack.append(tag_obj)
    return stack


def nu_checker_validation(filename, task=None, offset=0):
    """run the HTML file against the checker, process output and set result feedback accordingly

    :param filename: HTML file to check
    :type filename: str
    :param offset: trick to skip lines of code that are not part of the actual student submission (doctype, head etc... are ignored to reflect line number as seen from student POV)
    :type offset: int
    """

    # * for details about checker options, read: https://validator.github.io/validator/#options
    # * for details about json output format, read: https://github.com/validator/validator/wiki/Output-%C2%BB-JSON#example
    pout = subprocess.check_output(shlex.split(f"java -jar /opt/vnu/vnu.jar --no-langdetect --stdout --exit-zero-always --format json {filename}"), encoding="utf-8")

    json_output = json.loads(pout)
    messages = json_output["messages"]

    # * only keeps actual errors; info messages etc are discarded
    errors = [{"line_number": msg.get('firstLine', msg.get('lastLine')) - offset, "message": re.sub(r"[“”]+", "``", msg.get('message'))} for msg in messages if msg.get('type') == "error"]
    sorted_errors = sorted(errors, key=operator.itemgetter('line_number'))
    if errors:
        if task == None:
            feedback.set_global_result("failed")
        else:
            feedback.set_problem_result("failed", task)
    return sorted_errors


def css_validator_validation(filename, task=None, offset=0):
    """run the HTML file against the checker, process output and set result feedback accordingly

    :param filename: HTML file to check
    :type filename: str
    :param offset: trick to skip lines of code that are not part of the actual student submission
    :type offset: int
    """

    # * for details about json output format, see: https://github.com/w3c/css-validator/blob/6874d1990af57d3260fdc2a9420b09077cf2ed06/org/w3c/css/css/json.properties
    process = subprocess.run(shlex.split(f"java -jar /opt/css-validator/css-validator.jar --lang=fr --output=json file:{filename}"), stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    json_out = json.loads(process.stdout)

    messages = json_out["cssvalidation"]["errors"] if "errors" in json_out["cssvalidation"] else []
    errors = [{"line_number": msg.get('line', offset) - offset, "message_type":  msg.get('type'), "message": re.sub(r"[“”]+", "``", msg.get('message')).rstrip(": ")} for msg in messages]

    if errors:
        if task == None:
            feedback.set_global_result("failed")
        else:
            feedback.set_problem_result("failed", task)

    return errors


if __name__ == "__main__":
    pass

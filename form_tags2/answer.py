expected_answers = {
    "date_number": [
        {'element_name': 'label', 'element_attr': {"for":"hours-played"}, 'element_text': "heure(s) de jeu :"},
        {'element_name': 'input', 'element_attr': {"type": "number", "id":"hours-played"}, 'element_text': ""}
    ],
    "step": [
        {'element_name': 'label', 'element_attr': {"for":"hours-played"}, 'element_text': "heure(s) de jeu :"},
        {'element_name': 'input', 'element_attr': {"type": "number", "id":"hours-played", "step":"0.25", "min":"0.5"}, 'element_text': ""}
    ],
    "checkbox": [
        {'element_name': 'fieldset', 'element_attr': {}, 'element_text': ""},
        {'element_name': 'legend', 'element_attr': {}, 'element_text': "via quel(s) vecteur(s) avez-vous entendu parler du jeu pour la première fois ?"},
        {'element_name': 'input', 'element_attr': {"type": "checkbox", "id":"friend"}, 'element_text': ""},
        {'element_name': 'label', 'element_attr': {"for":"friend"}, 'element_text': "un(e) ami(e)"},
        {'element_name': 'input', 'element_attr': {"type": "checkbox", "id":"pub"}, 'element_text': ""},
        {'element_name': 'label', 'element_attr': {"for":"pub"}, 'element_text': "des publicités"},
        {'element_name': 'input', 'element_attr': {"type": "checkbox", "id":"influencer"}, 'element_text': ""},
        {'element_name': 'label', 'element_attr': {"for":"influencer"}, 'element_text': "des influenceurs (youtube, twitch, ...)"},
        {'element_name': 'input', 'element_attr': {"type": "checkbox", "id":"other"}, 'element_text': ""},
        {'element_name': 'label', 'element_attr': {"for":"other"}, 'element_text': "autres"}
    ]
}
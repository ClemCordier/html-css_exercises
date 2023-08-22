expected_answers = {
    "label_input": [
        {'element_name': 'form', 'element_attr': {}, 'element_text': ""},
        {'element_name': 'label', 'element_attr': {}, 'element_text': "adresse mail:"},
        {'element_name': 'input', 'element_attr': {"type": "email"}, 'element_text': ""}
    ],
    "label_input_for": [
        {'element_name': 'form', 'element_attr': {}, 'element_text': ""},
        {'element_name': 'label', 'element_attr': {"for":"email-input"}, 'element_text': "adresse mail:"},
        {'element_name': 'input', 'element_attr': {"type": "email", "id":"email-input"}, 'element_text': ""}
    ],
    "input_password": [
        {'element_name': 'form', 'element_attr': {}, 'element_text': ""},
        {'element_name': 'label', 'element_attr': {"for":"email-input"}, 'element_text': "adresse mail:"},
        {'element_name': 'input', 'element_attr': {"type": "email", "id":"email-input"}, 'element_text': ""},
        {'element_name': 'label', 'element_attr': {"for":"password-input"}, 'element_text': "mot de passe:"},
        {'element_name': 'input', 'element_attr': {"type": "password", "id":"password-input"}, 'element_text': ""}
    ],
    "input_attributes": [
        {'element_name': 'form', 'element_attr': {}, 'element_text': ""},
        {'element_name': 'label', 'element_attr': {"for":"email-input"}, 'element_text': "adresse mail:"},
        {'element_name': 'input', 'element_attr': {"type": "email", "id":"email-input", "placeholder": "mail@address.com"}, 'element_text': ""},
        {'element_name': 'label', 'element_attr': {"for":"password-input"}, 'element_text': "mot de passe:"},
        {'element_name': 'input', 'element_attr': {"type": "password", "id":"password-input", "minlength":"8", "maxlength":"16"}, 'element_text': ""}
    ]
}
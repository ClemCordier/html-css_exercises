expected_answers = {
    "select": [
        # {'element_name': 'form', 'element_attr': {}, 'element_text': ""},
        {'element_name': 'label', 'element_attr': {"for":"overall-rating"}, 'element_text': "appréciation globale :"},
        {'element_name': 'select', 'element_attr': {"id":"overall-rating"}, 'element_text': ""},
        {'element_name': 'option', 'element_attr': {"selected":"selected", "disabled":"disabled", "hidden":""}, 'element_text': "-- sélectionnez une appréciation --"},
        {'element_name': 'option', 'element_attr': {}, 'element_text': "mauvais"},
        {'element_name': 'option', 'element_attr': {}, 'element_text': "moyen"},
        {'element_name': 'option', 'element_attr': {}, 'element_text': "bien"},
        {'element_name': 'option', 'element_attr': {}, 'element_text': "très bien"},
        {'element_name': 'option', 'element_attr': {}, 'element_text': "excellent"}
    ],
    "textarea": [
        # {'element_name': 'form', 'element_attr': {}, 'element_text': ""},
        {'element_name': 'label', 'element_attr': {"for":"detailed-review"}, 'element_text': "critique détaillée :"},
        {'element_name': 'textarea', 'element_attr': {"id":"detailed-review", "rows":"15", "cols":"80"}, 'element_text': ""}
    ]
}
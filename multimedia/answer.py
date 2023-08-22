expected_answers = {
    'audio1': [
        {'element_name': 'audio', 'element_attr': {"controls":"", "src":"https://github.com/clemcordier/html-css_course_resources/blob/main/audio.mp3?raw=true"}, 'element_text': ""}
    ],
    'audio2': [
        {'element_name': 'audio', 'element_attr': {"controls":""}, 'element_text': ""},
        {'element_name': 'source', 'element_attr': {"src":"https://github.com/clemcordier/html-css_course_resources/blob/main/audio.mp3?raw=true", "type":"audio/mpeg"}, 'element_text': ""},
        {'element_name': 'source', 'element_attr': {"src":"https://github.com/clemcordier/html-css_course_resources/blob/main/audio.wav?raw=true", "type":"audio/wav"}, 'element_text': ""}
    ],
    'audio3': [
        {'element_name': 'audio', 'element_attr': {"controls":""}, 'element_text': ""},
        {'element_name': 'source', 'element_attr': {"src":"https://github.com/clemcordier/html-css_course_resources/blob/main/audio.mp3?raw=true", "type":"audio/mpeg"}, 'element_text': ""},
        {'element_name': 'source', 'element_attr': {"src":"https://github.com/clemcordier/html-css_course_resources/blob/main/audio.wav?raw=true", "type":"audio/wav"}, 'element_text': "votre navigateur ne prend pas en charge les éléments audio. voici un"},
        {'element_name': 'p', 'element_attr': {}, 'element_text': "votre navigateur ne prend pas en charge les éléments audio. voici un lien de téléchargement direct."},
        {'element_name': 'a', 'element_attr': {"href":"https://github.com/clemcordier/html-css_course_resources/blob/main/audio.mp3?raw=true"}, 'element_text': "lien de téléchargement direct"}
    ],
    'video': [
        {'element_name': 'video', 'element_attr': {"loop":"", "autoplay":"", "muted":"", "src":"https://github.com/clemcordier/html-css_course_resources/blob/main/video.mp4?raw=true"}, 'element_text': ""}
    ]
}
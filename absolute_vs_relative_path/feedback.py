feedback_messages = {
    "qcm1":
        {
            "0": "Le chemin relatif ``../images/img_01.jpg`` ne remonte que d'un niveau dans l'arborescence de fichier, autrement dans le dossier ``nested/``. Le dossier ``images/`` n'est pas accessible depuis cet emplacement.",
            "1": "Le préfixe ``/`` du chemin absolu ``/projects/my_website_project/images/img_01.jpg`` fait référence à la racine du lecteur courant. Ce chemin est équivalent au chemin ``D:/projects/my_website_project/images/img_01.jpg``.",
            "2": "Le chemin relatif ``../../images/img_01.jpg`` remonte de 2 niveaux dans l'arborescence de fichier. Le premier ``../`` nous situe dans le dossier ``nested/``. Le second ``../`` nous situe dans le dossier ``my_website_project/``. De là, nous avons bien accès au dossier ``images/``.",
            "3": "Le chemin relatif ``./images/img_01.jpg`` n'est pas valide. Le ``./`` fait référence au dossier courant. Il aurait donc fallu que le dossier ``image/`` soit un sous-dossier du dossier courant, autrement dit un sous-dossier de ``folder/``.",
            "4": "Le chemin absolu ``D:/projects/my_website_project/images/img_01.jpg`` est valide."
        },
    "qcm2":
        {
            "0": "Le chemin ``../images/img_01.jpg`` ne remonte que d'un niveau dans l'arborescence de fichier, autrement dans le dossier ``nested/``. Le dossier ``images/`` n'est pas accessible depuis cet emplacement.",
            "1": "Le préfixe ``/`` du chemin absolu ``/projects/my_website_project/images/img_01.jpg`` fait référence à la racine du lecteur courant. Ce chemin est équivalent au chemin local ``D:/projects/my_website_project/images/img_01.jpg`` et ne sera donc pas accessible pour les utilisateurs en ligne.",
            "2": "Le chemin relatif ``../../images/img_01.jpg`` remonte de 2 niveaux dans l'arborescence de fichier. Le premier ``../`` nous situe dans le dossier ``nested/``. Le second ``../`` nous situe dans le dossier ``my_website_project/``. De là, nous avons bien accès au dossier ``images/``. Étant donné que ce chemin est relatif au projet et non au lecteur local, il sera donc valide aussi bien pour vous sur votre machine que pour tous les utilisateurs en ligne.",
            "3": "Le chemin relatif ``./images/img_01.jpg`` n'est pas valide. Le ``./`` fait référence au dossier courant. Il aurait donc fallu que le dossier ``image/`` soit un sous-dossier du dossier courant, autrement dit un sous-dossier de ``folder/``.",
            "4": "Le chemin absolu ``D:/projects/my_website_project/images/img_01.jpg`` ne sera pas accessible pour les utilisateurs en ligne."
        }
}
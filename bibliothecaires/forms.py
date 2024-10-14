from django import forms

MEDIA_TYPES = [
    ('livre', 'Livre'),
    ('dvd', 'DVD'),
    ('cd', 'CD'),
    ('jeux', 'Jeux de Plateau')
]

class Creationmedia(forms.Form):
    type_media = forms.ChoiceField(choices=MEDIA_TYPES, required=True)
    nom = forms.CharField(max_length=150)
    auteur = forms.CharField(max_length=150, required=False)
    realisateur = forms.CharField(max_length=150, required=False)
    artiste = forms.CharField(max_length=150, required=False)
    createur = forms.CharField(max_length=150, required=False)



class Updatemedia(forms.Form):
    nom = forms.CharField(required=True)
    auteur = forms.CharField(required=False)
    realisateur = forms.CharField(required=False)
    artiste = forms.CharField(required=False)
    createur = forms.CharField(required=False)


class Creationmembre(forms.Form):
    nom = forms.CharField(required=True)
    prenom = forms.CharField(required=True)



class Updatemembre(forms.Form):
    nom = forms.CharField(required=False)
    prenom = forms.CharField(required=False)
from django.utils import timezone
from datetime import timedelta
from django.db import models

class Media(models.Model):
    nom = models.CharField(max_length=150, default='Média par défaut')
    est_disponible = models.BooleanField(default=True)
    est_jeu_de_plateau = models.BooleanField(default=False)

    def __str__(self):
        return self.nom


class Livre(Media):
    auteur = models.fields.CharField(max_length=150)

class Jeuxdeplateau(Media):
    createur = models.CharField(max_length=150, default='Créateur inconnu')

class Dvd(Media):
    realisateur = models.fields.CharField(max_length=150)

class Cd(Media):
    artiste = models.fields.CharField(max_length=150)


class Membre(models.Model):
    nom = models.fields.CharField(max_length=150)
    prenom = models.fields.CharField(max_length=150)


def date_retour_7_jours():
    return timezone.now() + timedelta(days=7)


class Emprunt(models.Model):
    membre = models.ForeignKey(Membre, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(default=timezone.now)
    date_retour = models.DateTimeField(default=date_retour_7_jours)

    def est_en_retard(self):
        return timezone.now() > self.date_retour


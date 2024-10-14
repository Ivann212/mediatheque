import pytest
from django.urls import reverse
from .models import Media, Membre, Emprunt

@pytest.mark.django_db
def test_listemedias(client):
    response = client.get(reverse('listemedias'))  # Utilisation de reverse pour la redirection
    assert 'medias' in response.context


@pytest.mark.django_db
def test_deletemedia(client):
    media = Media.objects.create(nom='Test Media')
    response = client.post(reverse('deletemedia', args=[media.nom]))
    assert Media.objects.filter(nom='Test Media').count() == 0  # Vérifie que le média est supprimé

    # Test pour un média non existant
    response = client.post(reverse('deletemedia', args=['NonExistantMedia']))
    assert 'error_message' in response.context


@pytest.mark.django_db
def test_ajoutmedia(client):
    response = client.get(reverse('ajoutmedia'))  # URL pour ajouter un média

    # Test de la soumission du formulaire
    data = {
        'nom': 'Nouveau Média',
        'type_media': 'livre',
        'auteur': 'Auteur Test'
    }
    response = client.post(reverse('ajoutmedia'), data)
    assert Media.objects.filter(nom='Nouveau Média').exists()


@pytest.mark.django_db
def test_updatemedia(client):
    media = Media.objects.create(nom='Média à Modifier')
    data = {
        'nom': 'Média Modifié'
    }
    response = client.post(reverse('updatemedia', args=[media.nom]), data)
    assert Media.objects.get(nom='Média Modifié')  # Vérifie que le nom a été mis à jour


@pytest.mark.django_db
def test_ajoutmembre(client):
    response = client.get(reverse('ajoutmembre'))  # URL pour ajouter un membre

    # Test de la soumission du formulaire
    data = {
        'nom': 'Nom Test',
        'prenom': 'Prénom Test'
    }
    response = client.post(reverse('ajoutmembre'), data)
    assert Membre.objects.filter(nom='Nom Test').exists()


@pytest.mark.django_db
def test_updatemembre(client):
    membre = Membre.objects.create(nom='Membre', prenom='Test')
    data = {
        'nom': 'Membre Modifié',
        'prenom': 'Test Modifié'
    }
    response = client.post(reverse('updatemembre', args=[membre.id]), data)
    updated_membre = Membre.objects.get(id=membre.id)
    assert updated_membre.nom == 'Membre Modifié'


@pytest.mark.django_db
def test_deletemembre(client):
    membre = Membre.objects.create(nom='Membre à Supprimer', prenom='Test')
    response = client.post(reverse('deletemembre', args=[membre.id]))
    assert Membre.objects.filter(id=membre.id).count() == 0  # Vérifie que le membre est supprimé

    # Test pour un membre non existant
    response = client.post(reverse('deletemembre', args=[999]))  # ID inexistant
    assert 'error_message' in response.context


@pytest.mark.django_db
def test_creer_emprunt(client):
    membre = Membre.objects.create(nom='Membre Emprunteur', prenom='Test')
    media = Media.objects.create(nom='Média Empruntable', est_disponible=True)
    data = {
        'membre_nom': membre.nom,
        'membre_prenom': membre.prenom,
        'media_nom': media.nom
    }

    # Test de création d'un emprunt
    response = client.post(reverse('creer_emprunt'), data)
    assert Emprunt.objects.filter(membre=membre, media=media).exists()

    # Test d'emprunt d'un média non disponible
    media.est_disponible = False
    media.save()
    response = client.post(reverse('creer_emprunt'), data)
    assert 'message' in response.context


@pytest.mark.django_db
def test_retourner_media(client):
    membre = Membre.objects.create(nom='Membre Retour', prenom='Test')
    media = Media.objects.create(nom='Média à Retourner', est_disponible=False)
    emprunt = Emprunt.objects.create(membre=membre, media=media)

    data = {
        'membre_nom': membre.nom,
        'membre_prenom': membre.prenom,
        'media_nom': media.nom
    }
    response = client.post(reverse('retourner_media'), data)
    assert Emprunt.objects.filter(membre=membre, media=media).count() == 0  # Vérifie que l'emprunt est supprimé
    assert media.est_disponible  # Vérifie que le média est maintenant disponible


@pytest.mark.django_db
def test_liste_emprunts(client):
    response = client.get(reverse('liste_emprunts'))  # URL pour la liste des emprunts
    assert 'emprunts' in response.context

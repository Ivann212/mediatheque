from django.contrib.auth.decorators import  user_passes_test
from .forms import Creationmedia, Updatemedia, Creationmembre, Updatemembre
from .models import Media, Membre, Emprunt, Livre, Cd, Dvd, Jeuxdeplateau
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import logout


def listemedias(request):
    medias = Media.objects.all()
    return render(request, 'medias/lists.html', {'medias': medias})



def is_bibliothécaire(user):
    return user.is_authenticated and user.username == 'Bibliothécaire'


def deletemedia(request, nom):
    try:
        # Recherche du média avec le nom donné
        media = Media.objects.get(nom=nom)
        # Suppression du média
        media.delete()
        # Redirection après suppression
        return redirect('listemedias')  # 'medias_liste' doit être défini dans urls.py pour la liste des médias
    except Media.DoesNotExist:
        # Si le média n'existe pas, afficher un message d'erreur
        return render(request, 'medias/lists.html', {
            'medias': Media.objects.all(),
            'error_message': f"Le média '{nom}' n'existe pas."
        })

def ajoutmedia(request):
        if request.method == 'POST':
            creationmedia = Creationmedia(request.POST)
            if creationmedia.is_valid():
                type_media = creationmedia.cleaned_data['type_media']
                nom = creationmedia.cleaned_data['nom']

                # Créer le bon type de média
                if type_media == 'livre':
                    Livre.objects.create(nom=nom, auteur=creationmedia.cleaned_data['auteur'])
                elif type_media == 'dvd':
                    Dvd.objects.create(nom=nom, realisateur=creationmedia.cleaned_data['realisateur'])
                elif type_media == 'cd':
                    Cd.objects.create(nom=nom, artiste=creationmedia.cleaned_data['artiste'])
                elif type_media == 'jeux':
                    Jeuxdeplateau.objects.create(nom=nom, createur=creationmedia.cleaned_data['createur'], est_disponible=False)

                return redirect('listemedias')  # Assure-toi que cela correspond à ta route
        else:
            creationmedia = Creationmedia()

        return render(request, 'medias/ajoutmedia.html', {'creationmedia': creationmedia})



def updatemedia(request, nom):
    try:
        # Recherche du média avec le nom donné
        media = Media.objects.get(nom=nom)

        # Si la requête est de type POST, cela signifie que le formulaire a été soumis
        if request.method == 'POST':
            form = Updatemedia(request.POST)

            # Si le formulaire est valide, on met à jour les informations du média
            if form.is_valid():
                media.nom = form.cleaned_data['nom']

                # Mise à jour des champs spécifiques en fonction du type de média
                if isinstance(media, Livre):
                    media.auteur = form.cleaned_data.get('auteur', media.auteur)
                elif isinstance(media, Dvd):
                    media.realisateur = form.cleaned_data.get('realisateur', media.realisateur)
                elif isinstance(media, Cd):
                    media.artiste = form.cleaned_data.get('artiste', media.artiste)
                elif isinstance(media, Jeuxdeplateau):
                    media.createur = form.cleaned_data.get('createur', media.createur)

                # Sauvegarde du média après les modifications
                media.save()

                # Redirection vers la liste des médias après mise à jour
                return redirect('listemedias')

        else:
            # Si la requête est de type GET, on affiche le formulaire avec les informations actuelles
            initial_data = {
                'nom': media.nom,
                'auteur': getattr(media, 'auteur', ''),
                'realisateur': getattr(media, 'realisateur', ''),
                'artiste': getattr(media, 'artiste', ''),
                'createur': getattr(media, 'createur', ''),
            }
            form = Updatemedia(initial=initial_data)

        return render(request, 'medias/update.html', {'form': form, 'media': media})

    except Media.DoesNotExist:
        # Si le média n'existe pas, on affiche un message d'erreur
        return render(request, 'medias/lists.html', {
            'medias': Media.objects.all(),
            'error_message': f"Le média '{nom}' n'existe pas."
        })



def ajoutmembre(request):
    membres = Membre.objects.all()

    if request.method == 'POST':
        creationmembre = Creationmembre(request.POST)
        if creationmembre.is_valid():
            membre = Membre()
            membre.nom = creationmembre.cleaned_data['nom']
            membre.prenom = creationmembre.cleaned_data['prenom']
            membre.save()
            membres = Membre.objects.all()
            return render(request, 'medias/membre.html', {'creationMembre': creationmembre, 'membres': membres})
    else:
        creationmembre = Creationmembre()
    return render(request, 'medias/membre.html', {'creationMembre': creationmembre, 'membres': membres})


def updatemembre(request, id):
    membre = get_object_or_404(Membre, id=id)

    if request.method == 'POST':
        updatemembre = Updatemembre(request.POST)
        if updatemembre.is_valid():
            membre.nom = updatemembre.cleaned_data['nom']
            membre.prenom = updatemembre.cleaned_data['prenom']
            membre.save()  # N'oublie pas de sauvegarder les modifications
            return redirect('ajoutmembre')  # Rediriger vers la liste des membres
    else:
        # Remplir le formulaire avec les données existantes
        initial_data = {
            'nom': membre.nom,
            'prenom': membre.prenom,
        }
        updatemembre = Updatemembre(initial=initial_data)

    return render(request, 'medias/updatemembre.html', {'updatemembre': updatemembre})




def deletemembre(request, id):
    try:
        membre = Membre.objects.get(id=id)
        membre.delete()
        return redirect('ajoutmembre')
    except Membre.DoesNotExist:
        return render(request, 'medias/membre.html', {
            'membres': Membre.objects.all(),
            'error_message': "Le membre n'existe pas."
        })


def creer_emprunt(request):
    if request.method == 'POST':
        membre_nom = request.POST.get('membre_nom')
        membre_prenom = request.POST.get('membre_prenom')
        media_nom = request.POST.get('media_nom')

        # Chercher le membre correspondant
        membre = Membre.objects.filter(nom=membre_nom, prenom=membre_prenom).first()
        media = Media.objects.filter(nom=media_nom).first()

        if not membre or not media:
            return render(request, 'medias/creer_emprunt.html', {
                'emprunts': Emprunt.objects.all(),
                'error_message': "Le membre ou le média n'existe pas."
            })

        # Vérification des limites d'emprunt pour le membre
        emprunts_en_cours = Emprunt.objects.filter(membre=membre, date_retour__gte=timezone.now())
        if emprunts_en_cours.count() >= 3:
            return render(request, 'medias/erreur.html', {
                'emprunts': Emprunt.objects.all(),
                'message': "Le membre a déjà 3 emprunts en cours."
            })

        # Vérifier que le média est disponible
        if not media.est_disponible:
            return render(request, 'medias/erreur.html', {
                'emprunts': Emprunt.objects.all(),
                'message': "Le média est déjà emprunté."
            })

        # Vérifier si le média est un jeu de plateau
        if media.est_jeu_de_plateau:
            return render(request, 'medias/creer_emprunt.html', {
                'medias': Media.objects.filter(est_disponible=True),  # Filtrer les médias disponibles
                'membres': Membre.objects.all(),
                'error_message': "Les jeux de plateau ne peuvent pas être empruntés."
            })

        # Créer l'emprunt et marquer le média comme emprunté
        emprunt = Emprunt(membre=membre, media=media)
        emprunt.save()

        media.est_disponible = False
        media.save()

        return redirect('creer_emprunt')

    # Si méthode GET, retourner la page avec la liste des membres et médias
    emprunts = Emprunt.objects.all()
    membres = Membre.objects.all()
    medias = Media.objects.filter(est_disponible=True)

    return render(request, 'medias/creer_emprunt.html', {
        'emprunts': emprunts,
        'membres': membres,
        'medias': medias
    })



def retourner_media(request):
    if request.method == 'POST':
        membre_nom = request.POST['membre_nom']
        membre_prenom = request.POST['membre_prenom']
        media_nom = request.POST['media_nom']

        # Chercher le membre correspondant
        try:
            membre = Membre.objects.get(nom=membre_nom, prenom=membre_prenom)
        except Membre.DoesNotExist:
            return render(request, 'medias/erreur.html', {'message': "Le membre n'existe pas."})

        # Chercher l'emprunt correspondant
        try:
            emprunt = Emprunt.objects.get(membre=membre, media__nom=media_nom)
        except Emprunt.DoesNotExist:
            return render(request, 'medias/erreur.html', {'message': "Cet emprunt n'existe pas."})

        media = emprunt.media
        media.est_disponible = True
        media.save()
        emprunt.delete()

        return redirect('liste_emprunts')

    return render(request, 'medias/retourner_media.html')


def liste_emprunts(request):
    emprunts = Emprunt.objects.all()
    return render(request, 'medias/emprunt.html', {'emprunts': emprunts})

def custom_logout(request):
    logout(request)
    return redirect('listemedias')












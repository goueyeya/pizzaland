from django.shortcuts import render, redirect
from applicompte.models import PizzaUser
from applipanier.models import Commande, LigneCommande
from applipizza.models import Pizza
from math import ceil

# Create your views here.
def revenus(request) :
    user = None
    if request.user.is_staff:
        user =  PizzaUser.objects.get(id = request.user.id)
        # le user (ici ce sera un administrateur)
        # la requête écrite "à la main". Notez les triples
        # guillemets pour écrire une string sur plusieurs lignes 
        requete='''
        SELECT *
        FROM applipanier_commande WHERE payee = 1
        AND julianday (date()) - julianday (dateCommande) <= 7 ORDER BY dateCommande;
        '''
        # exécution de la requête
        lesCommandesPayees = Commande.objects.raw(requete)

        # bd vide apres 7 jours
        if len(lesCommandesPayees) == 0:
            requete='''SELECT * FROM applipanier_commande WHERE payee = 1 ORDER BY dateCommande;'''
            lesCommandesPayees = Commande.objects.raw(requete)

        # initialisation des variables qui seront utilisées # par le cript js via des variables de gabarit 
        lesDatesDesCommandes = []
        lesMontantsDesCommandes = []
        CAmax = 0

        # l'algorithme pour qu'à un même indice i on ait # - la date de la commande dans la première liste # - le montant de la commande dans la deuxième liste 
        for commande in lesCommandesPayees :
            laDate = commande.dateCommande.strftime('%d/%m/%Y') 
            leMontant = float(commande.prix)
            if laDate not in lesDatesDesCommandes : 
                lesDatesDesCommandes.append(laDate)
                lesMontantsDesCommandes.append(leMontant)
            else:
                n = lesDatesDesCommandes.index (laDate) 
                lesMontantsDesCommandes[n] += leMontant

        # calcul du montant maximum pour adapter l'échelle des y du graphique 
        for montant in lesMontantsDesCommandes :
            if montant > CAmax :
                CAmax = montant

        # calcul de la graduation max pour l'axe des y
        # par exemple CAmax = 385 donne 385 // 50 = 7, 750 + 50 = 400 
        CAmax = ceil(CAmax // 50) * 50 + 50
        # appel du template
        return render(
            request,
            'applistats/revenus.html',
            {"dates": lesDatesDesCommandes, "montants" : lesMontantsDesCommandes, "user": user, "CAmax" : CAmax}
        )
    else:
        return redirect('/login')
    
def ventes(request):
    user = None
    if request.user.is_staff:
        user =  PizzaUser.objects.get(id = request.user.id)
        # le user (ici ce sera un administrateur)
        # la requête écrite "à la main". Notez les triples
        # guillemets pour écrire une string sur plusieurs lignes 
        requete='''
        SELECT *
        FROM applipanier_commande WHERE payee = 1
        AND julianday (date()) - julianday (dateCommande) <= 7 ORDER BY dateCommande;
        '''    
                # exécution de la requête
        lesCommandesPayees = Commande.objects.raw(requete)

        # bd vide apres 7 jours
        if len(lesCommandesPayees) == 0:
            requete='''SELECT * FROM applipanier_commande WHERE payee = 1 ORDER BY dateCommande;'''
            lesCommandesPayees = Commande.objects.raw(requete)


        # initialisation des variables qui seront utilisées # par le cript js via des variables de gabarit 
        nomDesPizzas = []
        ventesDesPizzas = []

        # l'algorithme pour qu'à un même indice i on ait # - la date de la commande dans la première liste # - le montant de la commande dans la deuxième liste 
        for commande in lesCommandesPayees :
            lesLignesCommande = LigneCommande.objects.filter(commande = commande.idCommande)
            for ligne in lesLignesCommande : 
                nom = ligne.pizza.nomPizza
                qte = ligne.quantite
                if nom not in nomDesPizzas:
                    nomDesPizzas.append(nom)
                    ventesDesPizzas.append(int(qte))
                else:
                    n = nomDesPizzas.index(nom) 
                    ventesDesPizzas[n] += int(qte)
        
        return render(
            request,
            'applistats/ventes.html',
            {"noms": nomDesPizzas, "ventes" : ventesDesPizzas, "user": user}
        )
    else:
        return redirect('/login')
    
def recent_activities(request):
    user = None
    if request.user.is_staff:
        user =  PizzaUser.objects.get(id = request.user.id)

        requete='''
            SELECT *
            FROM applipanier_commande WHERE payee = 1
            AND julianday (date()) - julianday (dateCommande) <= 7 ORDER BY dateCommande;
            '''  
        
        # exécution de la requête
        lesCommandesPayees = Commande.objects.raw(requete)

        # bd vide apres 7 jours
        if len(lesCommandesPayees) == 0:
            requete = '''SELECT * FROM applipanier_commande WHERE payee = 1 ORDER BY dateCommande;'''
            lesCommandesPayees = Commande.objects.raw(requete)

        nomDesPizzas = []
        ventesDesPizzas = []
        nbCommande = 0
        ChA = 0

        for commande in lesCommandesPayees :
            lesLignesCommande = LigneCommande.objects.filter(commande = commande.idCommande)
            nbCommande += 1
            ChA += commande.prix
            for ligne in lesLignesCommande : 
                nom = ligne.pizza.nomPizza
                qte = ligne.quantite
                if nom not in nomDesPizzas:
                    nomDesPizzas.append(nom)
                    ventesDesPizzas.append(int(qte))
                else:
                    n = nomDesPizzas.index(nom) 
                    ventesDesPizzas[n] += int(qte)

        # meilleur vente
        meilleur_vente = nomDesPizzas[0]
        best_nb_vente = ventesDesPizzas[0]
        for pizza in nomDesPizzas:
            if ventesDesPizzas[nomDesPizzas.index(pizza)] > best_nb_vente : 
                meilleur_vente = pizza
                best_nb_vente = ventesDesPizzas[nomDesPizzas.index(pizza)]
        img_best_vente = Pizza.objects.get(nomPizza = meilleur_vente).image

        #panier moyen 
        panier_moyen = round(ChA / nbCommande, 2) 

        lesDatesDesCommandes = []
        lesMontantsDesCommandes = []
        CAmax = 0

        # l'algorithme pour qu'à un même indice i on ait # - la date de la commande dans la première liste # - le montant de la commande dans la deuxième liste 
        for commande in lesCommandesPayees :
            laDate = commande.dateCommande.strftime('%d/%m/%Y') 
            leMontant = float(commande.prix)
            if laDate not in lesDatesDesCommandes : 
                lesDatesDesCommandes.append(laDate)
                lesMontantsDesCommandes.append(leMontant)
            else:
                n = lesDatesDesCommandes.index (laDate) 
                lesMontantsDesCommandes[n] += leMontant

        # calcul du montant maximum pour adapter l'échelle des y du graphique 
        for montant in lesMontantsDesCommandes :
            if montant > CAmax :
                CAmax = montant

        # calcul de la graduation max pour l'axe des y
        # par exemple CAmax = 385 donne 385 // 50 = 7, 750 + 50 = 400 
        CAmax = ceil(CAmax // 50) * 50 + 50

        return render(
            request,
            'applistats/activitesrecentes.html',
            {"best_sale": meilleur_vente, 
             "best_nb_sale" : best_nb_vente, 
             "best_sale_img" : img_best_vente,
             "nb_commande" : nbCommande,
             "panier_moyen" : panier_moyen,
             "noms": nomDesPizzas, 
             "ventes" : ventesDesPizzas,
             "dates": lesDatesDesCommandes, 
             "montants" : lesMontantsDesCommandes, 
             "CAmax" : CAmax,
             "user": user}
        )

    else:
        return redirect('/login')
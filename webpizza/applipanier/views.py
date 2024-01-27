from django.shortcuts import render, redirect
from applicompte.models import PizzaUser
from applipanier.models import Commande, LigneCommande
from applipizza.models import Pizza

# Create your views here.

def afficherPanier(request) :
    user = None
    if request.user.is_authenticated and not request.user.is_staff: 
        user = PizzaUser.objects.get(id = request.user.id)
        commandesNP = Commande.objects.filter(pizzauser = user).filter(payee = False)

        if len(commandesNP)  != 0 :
            panier = commandesNP.first()
            lesLignesDuPanier = LigneCommande.objects.filter(commande_id = panier.idCommande)
        else:
            panier = None
            lesLignesDuPanier = None 
        return render(request, 'applipanier/panier.html', {'user' : user, 'panier' : panier, 'lesLignesDuPanier' : lesLignesDuPanier})
    else:
        return redirect('/login')
    
def ajouterPizzaAuPanier(request, pizza_id):
    user = None
    if request.user.is_authenticated and not request.user.is_staff: 
        user = PizzaUser.objects.get(id = request.user.id)
        piz = Pizza.objects.get(idPizza = pizza_id)

        # c. on récupère le panier actuel, au besoin on le crée
        commandesNP = Commande.objects.filter(pizzauser=user, payee=False)

        if commandesNP.exists():
            panier = commandesNP.first()
        else:
            panier = Commande.objects.create(pizzauser=user, payee=False, prix=0)

        # d. on ajoute au prix du panier celui de la pizza, et on sauvegarde le panier
        panier.prix += piz.prix
        panier.save()

         # e. on récupère les lignes de ce panier, puis la ligne du panier concernant cette pizza
        lesLignesDuPanier = LigneCommande.objects.filter(commande_id=panier)
        lesLignesExistantes = lesLignesDuPanier.filter(pizza=piz)

        # f. si une telle ligne existe, on augmente sa quantité de 1, son prix du prix de la pizza, et on sauvegarde cette ligne
        if lesLignesExistantes.exists():
            ligne_pizza = lesLignesExistantes.first()
            ligne_pizza.quantite += 1
            ligne_pizza.prix += piz.prix
            ligne_pizza.save()
        else:
            # g. sinon, on la crée, on affecte à son attribut pizza la pizza ajoutée, à sa quantité la valeur 1, à son prix le prix de la pizza, à son attribut commande le panier en cours, et on sauvegarde la ligne
            LigneCommande.objects.create(
                quantite=1,
                prix=piz.prix,
                commande=panier,
                pizza=piz
            )
        
        return redirect('/cart')
    else:
        redirect('/login')

def retirerDuPanier(request, pizza_id):
    user = None
    if request.user.is_authenticated and not request.user.is_staff:
        user = PizzaUser.objects.get(id=request.user.id)

        # b. on récupère le panier actuel,
        commandesNP = Commande.objects.filter(pizzauser=user, payee=False)
        if commandesNP.exists():
            panier = commandesNP.first()
        else:
            return redirect('/cart')

        # c. on récupère la pizza à retirer,
        pizza = Pizza.objects.get(idPizza=pizza_id)

        # d. on récupère la ligne du panier qui concerne cette pizza,
        ligne_pizza = LigneCommande.objects.filter(commande=panier, pizza=pizza).first()

        if ligne_pizza:
            # e. on récupère la quantité de cette ligne,
            quantite_retiree = ligne_pizza.quantite

            # f. on supprime la ligne,
            ligne_pizza.delete()

            # g. on modifie le prix total du panier
            panier.prix -= quantite_retiree * pizza.prix
            panier.save()

            # h. on rerécupère les lignes du panier,
            lesLignesDuPanier = LigneCommande.objects.filter(commande=panier)

            # j. s’il n’y en a plus aucune, on supprime le panier, on le met à None, ainsi que lesLignesDuPanier,
            if not lesLignesDuPanier.exists():
                panier.delete()
                panier = None
                lesLignesDuPanier = None

            # k. ensuite, on retourne le render avec comme template panier.html, et comme contenu les lignes du panier, le panier et le user.
            return redirect('/cart')
        else:
            # Gérez le cas où la ligne n'existe pas (la pizza n'est pas dans le panier)
            return redirect('/cart')
    else:
        return redirect('/login')
    
def viderPanier(request):
    user = None
    if request.user.is_authenticated and not request.user.is_staff:
        user = PizzaUser.objects.get(id=request.user.id)

        # b. on récupère le panier actuel,
        commandesNP = Commande.objects.filter(pizzauser=user, payee=False)
        if commandesNP.exists():
            panier = commandesNP.first()
        else:
            # Si le panier n'existe pas, redirigez ou gérez le cas en conséquence
            return redirect('/panier')

        # c. on supprime le panier, ce qui, par les contraintes en CASCADE, va supprimer les lignes de ce panier,
        panier.delete()

        # d. on met le panier à None, ainsi que lesLignesDuPanier,
        panier = None
        lesLignesDuPanier = None

        # e. ensuite, on retourne le render avec comme template panier.html, et comme contenu les lignes du panier, le panier et le user.
        return redirect('/cart')
    else:
        return redirect('/login')
    

def retirerUnePizzaDuPanier(request, pizza_id):
    user = None
    if request.user.is_authenticated and not request.user.is_staff:
        user = PizzaUser.objects.get(id=request.user.id)

        # b. on récupère le panier actuel,
        commandesNP = Commande.objects.filter(pizzauser=user, payee=False)
        if commandesNP.exists():
            panier = commandesNP.first()
        else:
            return redirect('/cart')

        # c. on récupère la pizza à retirer,
        pizza = Pizza.objects.get(idPizza=pizza_id)

        # d. on récupère la ligne du panier qui concerne cette pizza,
        ligne_pizza = LigneCommande.objects.filter(commande=panier, pizza=pizza).first()

        if ligne_pizza:
            # e. on récupère la quantité de cette ligne,
            quantite_retiree = ligne_pizza.quantite

            # f. on modifie le prix total du panier en lui retirant le prix de la pizza supprimée,
            panier.prix -= pizza.prix

            if quantite_retiree == 1:
                # g. si la quantité récupérée est 1, on supprime la ligne
                ligne_pizza.delete()
            else:
                # h. sinon on diminue la quantité de 1, on diminue le prix de la ligne du prix de la pizza, et on sauvegarde la ligne
                ligne_pizza.quantite -= 1
                ligne_pizza.prix -= pizza.prix
                ligne_pizza.save()

            # i. on sauvegarde le panier,
            panier.save()

            # j. on rerécupère les lignes du panier,
            lesLignesDuPanier = LigneCommande.objects.filter(commande=panier)

            # k. s’il n’y en a plus aucune, on supprime le panier, on le met à None, ainsi que lesLignesDuPanier,
            if not lesLignesDuPanier.exists():
                panier.delete()
                panier = None
                lesLignesDuPanier = None

            # l. ensuite, on retourne le render avec comme template panier.html, et comme contenu les lignes du panier, le panier et le user.
            return redirect('/cart')
        else:
            return redirect('/cart')
    else:
        return redirect('/login')
    
def payerPanier(request):
    user = None
    if request.user.is_authenticated and not request.user.is_staff:
        user = PizzaUser.objects.get(id=request.user.id)

        # b. on récupère le panier actuel,
        commandesNP = Commande.objects.filter(pizzauser=user, payee=False)
        if commandesNP.exists():
            panier = commandesNP.first()
        else:
            # Si le panier n'existe pas, redirigez ou gérez le cas en conséquence
            return redirect('/cart')

        # c. on passe l’attribut "payee" du panier à True,
        panier.payee = True

        # d. on sauvegarde le panier,
        panier.save()

        # e. ensuite, on retourne le render avec comme template avisPaiement.html, et comme contenu le panier et le user.
        return render(request, 'applipanier/avisPaiement.html', {'user': user, 'panier': panier})
    else:
        return redirect('/login')
    
def afficherHistorique(request):
    user = None
    if request.user.is_authenticated:
        user = PizzaUser.objects.get(id=request.user.id)

        # on récupère ls commandes payées
        commandesP = Commande.objects.filter(pizzauser=user, payee=True)
        if commandesP.exists():
            return render(request, 'applipanier/historique.html', {'user': user, 'commandes': commandesP})
        else:
            # Si aucune commandes payées
            commandes = None
            return render(request, 'applipanier/historique.html', {'user': user, 'commandes': commandes})
    else:
        return redirect('/login')
    
def afficherCommande(request, commande_id):
    user = None
    if request.user.is_authenticated:
        user = PizzaUser.objects.get(id=request.user.id)

        commande = Commande.objects.filter(idCommande=commande_id)
        if commande.exists():
            commande = Commande.objects.filter(idCommande=commande_id).first()
            lignes_commande = LigneCommande.objects.filter(commande=commande)
            return render(request, 'applipanier/details_commande.html', {"commande" : commande, "lignes_commande" : lignes_commande})
        else:
            redirect('/orders')
    else:
        return redirect('/login')
    
def clients(request):
    user = None
    if request.user.is_staff:
        user = PizzaUser.objects.get(id=request.user.id)
        lesClients = PizzaUser.objects.filter(is_staff = False).order_by('date_joined')
        return render (
            request,
            'applipanier/clients.html',
            {"clients" : lesClients, "user" : user}
        )
    else:
        return redirect('/login')
    
def historiqueToutesCommandes(request):
    user = None
    if request.user.is_staff:
        user = PizzaUser.objects.get(id=request.user.id)
        lesCommandePayees = Commande.objects.all().filter(payee = True).order_by('dateCommande')
        return render (
            request,
            'applipanier/historiqueToutesCommandes.html',
            {"commandes" : lesCommandePayees, "user" : user}
        )
    else:
        return redirect('/login')
    
def afficherCommandesUtilisateur(request, user_id):
    user = None
    if request.user.is_staff:
        user = PizzaUser.objects.get(id=request.user.id)
        leClient = PizzaUser.objects.get(id=user_id)
        lesCommandePayeesDuClient = Commande.objects.all().filter(payee = True, pizzauser=leClient).order_by('dateCommande')
        return render (
            request,
            'applipanier/historique.html',
            {"commandes" : lesCommandePayeesDuClient, "user" : user}
        )
    else:
        return redirect('/login')

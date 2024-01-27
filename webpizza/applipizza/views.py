from django.shortcuts import render, redirect
#import des modèles
from applipizza.models import Pizza, Ingredient, Composition
from applicompte.models import PizzaUser
from applipizza.forms import IngredientForm, PizzaForm, CompositionForm
#import des user
from django.contrib.auth.models import User

# Create your views here.
def home(request):
    user = None
    if request.user.is_authenticated:
        user =  PizzaUser.objects.get(id = request.user.id)
    return redirect('/pizzas', user = user)


def pizzas(request) :
    user = None
    if request.user.is_authenticated:
        user =  PizzaUser.objects.get(id = request.user.id)
    #récuperation des pizzas de la bd -> même que ds le shell
    lesPizzas = Pizza.objects.all()

    #retouner l'emplacement du template, request pas utilisé
    #contenu calculé (lesPizzas) -> dict python
    return render (
        request,
        'applipizza/pizzas.html',
        {'pizzas': lesPizzas, "user" : user}
    )

def ingredients(request) :
    #creation du user 
    user= None

    # staff
    if request.user.is_staff :
        #récuperation des ingrédients de la bd -> même que ds le shell
        lesIngredients = Ingredient.objects.all()
        user = PizzaUser.objects.get(id = request.user.id)
        #retouner l'emplacement du template, request pas utilisé
        #contenu calculé (lesIngredients) -> dict python
        return render (
            request,
            'applipizza/ingredients.html',
            {'ingredients': lesIngredients, 'user' : user}
        )
    elif request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
        lesPizzas = Pizza.objects.all()
        return redirect('/pizzas/', user=user)
    else:
        return redirect('/login/', user=user)

def pizza(request, pizza_id) :
    user = None
    if request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
    # récupération de la pizza dont l'identifiant a été passé
    # en paramètre (c'est l'int pizza_id)
    laPizza = Pizza.objects.get(idPizza = pizza_id)

    # récupération des ingrédients entrant dans la composition de la pizza
    compo = Composition.objects.filter(pizza = pizza_id)

    # récupération de tous les ingrédients présent dans la BD
    ingredients = Ingredient.objects.all()

    # on crée un dictionnaire dont chaque item sera lui-même
    # un dictionnaire contenant :
    lesIngredients = [
        {
            'idCompo' :        c.idComposition,     # - l'identifiant de la composition (idComposition)
            'nomIngredient' : (Ingredient.objects.get(idIngredient = c.ingredient_id)).nomIngredient,    # - le nom de l'ingrédient
            'quantite' :      c.quantite      # - la quantité de l'ingrédient dans cette composition
        }
        for c in compo
    ]

    # on retourne l'emplacement du template, la pizza récupérée de la base
    # et la liste des ingrédients calculée ci-dessus
    return render (
        request,
        'applipizza/pizza.html',
        {
            'pizza': laPizza,
            'ingredientsPizza' : lesIngredients,
            'ingredients' : ingredients,
            'user' : user
        }
    )

def formulaireCreationIngredient(request):
    user = None
    if request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
    if request.user.is_staff:
        # indique l'emplacement du template
        return render (
            request,
            'applipizza/formulaireCreationIngredient.html',
            {'user' : user}
        )
    else:
        return redirect('/pizzas/', user)

def creerIngredient(request):
    user = None
    if request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
    if request.user.is_staff:
        # on récupère le formulaire
        form = IngredientForm(request.POST)

        #verifier si le fromulaire est valide 
        if form.is_valid():
            #récupération de la valeur nomIngredient
            #cleandata() permet d'éviter les injections
            nomIng = form.cleaned_data['nomIngredient']

            #creation d'un nouvelm ingrédient
            ing = Ingredient()

            #affectation de son attribut nomIngredient
            ing.nomIngredient = nomIng

            #enregistrement de l'ingrédient dans la BD
            ing.save()

            #on retourne l'emplacement de la vue (ou plutot du
            #template au sens de django)+ contenu calculé (dic python)
            return render (
                request,
                'applipizza/traitementFormulaireCreationIngredient.html',
                {"nom" : nomIng, 'user' : user}
            )
        else:
            return render(request, 'applipizza/FormulaireNonValide.html', {"erreurs" : form.errors})
    else:
        return redirect('/pizzas/', user=user)

def formulaireCreationPizza(request):
    user = None
    if request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
    if request.user.is_staff:
        # indique l'emplacement du template
        return render (
            request,
            'applipizza/formulaireCreationPizza.html',
            {"user" : user}
        )
    else:
        return redirect('/pizzas/', user=user)

def creerPizza(request):
    user = None
    if request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
    if request.user.is_staff:
        # on récupère le formulaire
        form = PizzaForm(request.POST)

        #verifier si le fromulaire est valide 
        if form.is_valid():
            #récupération de la valeur nomIngredient
            #cleandata() permet d'éviter les injections
            nomPiz = form.cleaned_data['nomPizza']
            prixPiz = form.cleaned_data['prix']
            image = request.FILES['image'] if 'image' in request.FILES else 'imagesPizzas/default.png'

            #creation d'une nouvelle pizza
            piz = Pizza()

            #affectation de son attribut nomIngredient
            piz.nomPizza = nomPiz
            piz.prix = prixPiz
            piz.image = image

            #enregistrement de l'ingrédient dans la BD
            piz.save()

            #on retourne l'emplacement de la vue (ou plutot du
            #template au sens de django)+ contenu calculé (dic python)
            return render (
                request,
                'applipizza/traitementFormulaireCreationPizza.html',
                {"nom" : nomPiz, "user" : user}
            )
        else:
            return render(request, 'applipizza/FormulaireNonValide.html', {"erreurs" : form.errors})
    else:
        return redirect('/pizzas/', user=user)

def ajouterIngredientDansPizza(request, pizza_id):
    user = None
    if request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
    if request.user.is_staff:
        # on récupère le formulaire
        form = CompositionForm(request.POST)

        #verifier si le fromulaire est valide 
        if form.is_valid():
            #récupération des données postées 
            ing = form.cleaned_data['ingredient']
            qte = form.cleaned_data['quantite']
            piz = Pizza.objects.get(idPizza = pizza_id)
            compoPizza = Composition.objects.filter(pizza = pizza_id)
            lesIngredientsDeLaPizza = ((ligne.ingredient) for ligne in compoPizza)

            #vérifier si pa déja présent dans la composition sinon le delete
            if ing in lesIngredientsDeLaPizza:
                compo = Composition.objects.filter(pizza = pizza_id, ingredient = ing)
                compo.delete()

            #creation de la nouvelle instance de la omposition et remplissage des attributs
            compo = Composition()
            compo.ingredient = ing
            compo.quantite = qte
            compo.pizza = piz
            compo.save() #sauvegarder dans la base

            # on retourne l'emplacement du template, la pizza récupérée de la base
            # et la liste des ingrédients calculée ci-dessus
            return redirect('/pizzas/'+str(pizza_id)+'/', user=user)
        else:
            return render(request, 'applipizza/FormulaireNonValide.html', {"erreurs" : form.errors})
    else:
        return redirect('/pizzas/', user=user)

def supprimerPizza(request, pizza_id):
    user = None
    if request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
    if request.user.is_staff:
        piz = Pizza.objects.get(idPizza = pizza_id)

        #supprmer la pizza
        piz.delete()
        return redirect('/pizzas/', user=user)
    else:
        return redirect('/pizzas/',user=user)

def afficherFormulaireModificationPizza(request, pizza_id):
    user = None
    if request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
    if request.user.is_staff:
        pizza_a_modifier = Pizza.objects.get(idPizza = pizza_id)
        return render(
            request,
            'applipizza/formulaireModificationPizza.html', 
            {'pizza' : pizza_a_modifier, "user" : user}
    )
    else:
        return redirect('/pizzas/', user)

def modifierPizza(request, pizza_id):
    user = None
    if request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
    if request.user.is_staff:
        piz = Pizza.objects.get(idPizza = pizza_id)

        #récupération de la pizza passée par le formulaire
        form = PizzaForm(request.POST, request.FILES, instance = piz)

        if form.is_valid():
            piz.image = request.FILES['image'] if 'image' in request.FILES else piz.image
            piz.save()
            return render(
                request,
                'applipizza/traitementFormulaireModificationPizza.html',
                {'pizza' : piz, "user" : user}
            )
        else:
            return render(request, 'applipizza/FormulaireNonValide.html', {"erreurs" : form.errors})
    else:
        return redirect('/pizzas/', user=user)

def supprimerIngredient(request, ingredient_id):
    user = None
    if request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
    if request.user.is_staff:
        ing = Ingredient.objects.get(idIngredient = ingredient_id)
        #supprmer la pizza
        ing.delete()
        return redirect('/ingredients/', user=user)
    else:
        return redirect('/pizzas/', user=user)

def afficherFormulaireModificationIngredient(request, ingredient_id):
    user = None
    if request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
    if request.user.is_staff:
        ing_a_modif = Ingredient.objects.get(idIngredient = ingredient_id)
        return render(
            request,
            'applipizza/formulaireModificationIngredient.html', 
            {'ingredient' : ing_a_modif, "user" : user}
        )
    else:
        return redirect('/pizzas/', user=user)

def modifierIngredient(request, ingredient_id):
    user = None
    if request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
    if request.user.is_staff:
        ing = Ingredient.objects.get(idIngredient = ingredient_id)

        #récupération de la pizza passée par le formulaire
        form = IngredientForm(request.POST, instance = ing)

        if form.is_valid():
            ing.save()
            return render(
                request,
                'applipizza/traitementFormulaireModificationIngredient.html',
                {'ingredient' : ing, "user" : user}
            )
        else:
            return render(request, 'applipizza/FormulaireNonValide.html', {"erreurs" : form.errors})
    else:
        return redirect('/pizzas/', user=user)
    
def supprimerIngredientDansPizza(request, pizza_id, composition_id):
    user = None
    if request.user.is_authenticated : 
        user = PizzaUser.objects.get(id = request.user.id)
    if request.user.is_staff:
        # récupérer la composition à supprimer (méthode get)
        compo = Composition.objects.get(idComposition = composition_id)

        # appeler la méthode delete() sur cette composition
        compo.delete()
        
        return redirect('/pizzas/'+str(pizza_id)+'/', user=user)
    else:
        return redirect('/pizzas/', user=user)
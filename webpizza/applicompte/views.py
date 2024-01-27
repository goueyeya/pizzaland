from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate, logout
from applicompte.forms import PizzaUserForm
from applipizza.models import Pizza
from applicompte.models import PizzaUser
from django.contrib.auth import views as auth_views

# Create your views here.
def login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/')
    else:
        return auth_views.LoginView.as_view(template_name = 'applicompte/login.html')(request)

def connexion(request):
    if request.user.is_staff or request.user.is_authenticated:
        return redirect('/pizzas/')
    if request.method == "GET":
        return redirect('/login/')
    else:
        usr = request.POST['username']
        pwd = request.POST['password']
        user = authenticate(request, username = usr, password = pwd)
        if user is not None:
            auth_login(request, user)
            return redirect('/pizzas/', user=user)
        else:
            return redirect('/login/')

def deconnexion(request):
    user = None
    if request.user.is_staff or request.user.is_authenticated:
        logout(request)
        return render(
            request,
            'applicompte/logout.html'
        )
    else:
        return redirect('/pizzas/')

def formulaireProfil(request):
    user = None
    #si connecté
    if request.user.is_authenticated:
        user = PizzaUser.objects.get(id = request.user.id)
        return render(
            request,
            'applicompte/profil.html',
            {"user" : user}
        )
    # si pas connecté
    else:
        return redirect('/login/')
    
def traitementFormulaireProfil(request):
    user = None
        #si connecté
    if request.user.is_authenticated:
        user = PizzaUser.objects.get(id = request.user.id)
        form = PizzaUserForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            user = PizzaUser.objects.get(id = user.id)
        return redirect('/pizzas', user=user)
    # si pas connecté
    else:
        return redirect('/login/')
    
def formulaireInscription(request):
    user = None 
    if request.user.is_authenticated:
        user = PizzaUser.objects.get(id = request.user.id)
        return redirect('/user/update/', user = user)
    else:
        return render(
            request,
            'applicompte/formulaireInscription.html'
        )
    
def traitementFormulaireInscription(request):
# récupération des champs du formulaire
    fst = request.POST['first_name'] 
    lst = request.POST['last_name'] 
    usr = request.POST['username'] 
    eml = request.POST['email'] 
    pwd= request.POST['password'] 
    img = request.FILES['image']

    # création d'un PizzaUser 
    user = PizzaUser()

    # affectation des champs récupérés aux attributs du PizzaUser
    user.first_name = fst 
    user.last_name = lst
    user.username = usr
    user.email = eml
    user.set_password(pwd) 
    user.image = img

    # sauvegarde du PizzaUser dans la base de données 
    user.save()

    # connexion du PizzaUser
    auth_login(request, user)
    return redirect('/pizzas/', user=user)
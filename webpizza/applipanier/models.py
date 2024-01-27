from django.db import models
from applipizza.models import Pizza
from applicompte.models import PizzaUser

# Create your models here.
class Commande(models.Model) :
    #id est une clé primaire, n auto-increment => AutoField
    idCommande = models.AutoField(primary_key = True)

    #est une chaine de caractères => CharField
    dateCommande = models.DateField(auto_now=False, auto_now_add=True)

    #un booléen qui dit si elle est payée
    payee = models.BooleanField(default=False)

    prix = models.DecimalField ( max_digits = 6, decimal_places = 2, verbose_name = 'le prix')

    pizzauser = models.ForeignKey(PizzaUser, on_delete = models.CASCADE)

    # une méthode de type toString()
    def __str__(self) -> str : 
        return self.nomIngredient

class LigneCommande(models.Model):

    idLigneCommande = models.AutoField(primary_key = True)

    quantite = models.DecimalField ( max_digits = 4, decimal_places = 0, verbose_name = 'la quantité de pizza')
    
    prix = models.DecimalField ( max_digits = 6, decimal_places = 2, verbose_name = 'le prix')

    commande = models.ForeignKey(Commande, on_delete = models.CASCADE)

    pizza = models.ForeignKey(Pizza, on_delete = models.CASCADE)


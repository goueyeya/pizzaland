from django.db import models

# Create your models here.

class Ingredient(models.Model) :

    #idIngredient est une clé primaire, n auto-increment => AutoField
    idIngredient = models.AutoField(primary_key = True)

    #idIngredient est une chaine de caractères => CharField
    nomIngredient = models.CharField(max_length = 50, verbose_name = '''le nom de l'ingrédient''')

    # une méthode de type toString()
    def __str__(self) -> str : 
        return self.nomIngredient

class Pizza(models.Model) :

    #idPizza est une clé primaire, n auto-increment => AutoField
    idPizza = models.AutoField(primary_key = True)

    #nomPizza est une chaine de caractères => CharField
    nomPizza = models.CharField(max_length = 50, verbose_name = '''le nom de la pizza''')

    # le prix est décimal, maximum = 4 chiffres dont 2 décimales 
    prix = models.DecimalField ( max_digits = 4, decimal_places = 2, verbose_name = 'le prix')

    #image de la pizza 
    image = models.ImageField(default= 'imagesPizzas/default.png', upload_to='imagesPizzas/')

    # une méthode de type toString()
    def __str__(self) -> str : 
        return 'Pizza "' + self.nomPizza + '" (' + str(self.prix) + ' €)'

class Composition(models.Model) :
    #la classe Meta qui gère l'unicité du couple de clés étrangères 
    class Meta :
        unique_together = ('ingredient', 'pizza') # le nom des clés étrangères 

    #idComposition est la clé primaire
    idComposition = models.AutoField(primary_key = True)

    #les deux champs clés étrangères, dont les noms correspondent
    #aux classes respectives en minuscules
    ingredient = models.ForeignKey(Ingredient, on_delete = models.CASCADE)
    pizza = models.ForeignKey(Pizza, on_delete = models.CASCADE)

    #l'autre champ, chaînes de caractères 
    quantite = models.CharField(max_length = 100, verbose_name = 'la quantité')

    #une méthode de type toString
    def __str__(self) -> str :
        ing = self.ingredient
        piz = self.pizza
        return ing.nomIngredient + ' fait partie de la pizza ' + piz.nomPizza + ' (quantite : ' + self.quantite + ')'
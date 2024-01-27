from django.urls import path
from applipizza import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('pizzas/', views.pizzas),
    path('ingredients/', views.ingredients),
    path('pizzas/<int:pizza_id>/', views.pizza),
    path('ingredients/add/', views.formulaireCreationIngredient),
    path('ingredients/create/', views.creerIngredient),
    path('pizzas/add/', views.formulaireCreationPizza),
    path('pizzas/create/', views.creerPizza),
    path('pizzas/<int:pizza_id>/addIngredient/', views.ajouterIngredientDansPizza),
    path('pizzas/<int:pizza_id>/delete/', views.supprimerPizza),
    path('pizzas/<int:pizza_id>/update/', views.afficherFormulaireModificationPizza),
    path('pizzas/<int:pizza_id>/updated/', views.modifierPizza),
    path('ingredients/<int:ingredient_id>/delete/', views.supprimerIngredient),
    path('ingredients/<int:ingredient_id>/update/', views.afficherFormulaireModificationIngredient),
    path('ingredients/<int:ingredient_id>/updated/', views.modifierIngredient),
    path('pizzas/<int:pizza_id>/deleteIngredient/<int:composition_id>/',views.supprimerIngredientDansPizza),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
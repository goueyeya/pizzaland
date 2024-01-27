from django.urls import path
from applipanier import views


urlpatterns = [
    path('cart/', views.afficherPanier),
    path('pizzas/<int:pizza_id>/buy/', views.ajouterPizzaAuPanier),
    path('cart/<int:pizza_id>/delete/', views.retirerDuPanier),
    path('cart/delete/', views.viderPanier),
    path('cart/<int:pizza_id>/decrease/', views.retirerUnePizzaDuPanier),
    path('cart/pay/', views.payerPanier),
    path('orders/', views.afficherHistorique),
    path('orders/<int:commande_id>/', views.afficherCommande),
    path('customers/', views.clients),
    path('allorders/', views.historiqueToutesCommandes),
    path('customers/<int:user_id>/orders/', views.afficherCommandesUtilisateur),
]
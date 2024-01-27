from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from applistats import views

urlpatterns = [
    path('stats/revenus/', views.revenus),
    path('stats/ventes/', views.ventes),
    path('stats/activite/', views.recent_activities),

]


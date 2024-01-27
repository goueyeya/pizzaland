from django.forms import ModelForm
from applicompte.models import PizzaUser

class PizzaUserForm(ModelForm):
    class Meta:
        model = PizzaUser
        fields = ['username', 'first_name', 'last_name', 'email', 'image']

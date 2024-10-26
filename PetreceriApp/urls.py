from django.contrib.auth.views import LoginView
from django.urls import path
from django.views.generic import TemplateView

from PetreceriApp.forms import LoginForm
from PetreceriApp.views import *

urlpatterns = [
    path('home', HomeView.as_view(template_name='home.html'), name='home'),
    path('login', LoginView.as_view(template_name='login.html', form_class=LoginForm), name='login'),
    path('create_party', CreatePartyView.as_view(), name='create_party'),
    path('signup', SignupView.as_view(), name='signup'),
    path('add_task/<int:party_id>', AddTasksView.as_view(), name='add_task'),
]
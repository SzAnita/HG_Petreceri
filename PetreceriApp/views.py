from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, FormView, CreateView

from PetreceriApp.forms import SignUpForm, CreatePartyForm
from PetreceriApp.models import *


class HomeView(TemplateView):
    extra_context = {
        'auth': 'false'
    }
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['auth'] = 'true'
        context['parties'] = Party.objects.all()
        return context


class SignupView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = 'home'

    def form_valid(self, form):
        login(self.request, form.save())
        return HttpResponseRedirect(reverse('home'))


class CreatePartyView(CreateView):
    model = Party
    form_class = CreatePartyForm
    template_name = 'new_party.html'
    success_url = 'add_tasks.html'

    def form_valid(self, form):
        self.object = form.save()
        self.object.refresh_from_db()
        party_id = self.object.id
        return reverse('add_task', kwargs={'party_id':party_id})


class AddTasksView(TemplateView):
    template_name = 'add_tasks.html'

    def post(self, request):
        party = Party.objects.get(id=request.POST['party_id'])
        task = Tasks(name=request.POST['task_name'], description=request.POST['task_desc'], person=request.POST['task_person'])




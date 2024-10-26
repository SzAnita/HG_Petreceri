from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.forms import forms, fields, PasswordInput
from django.utils.translation import gettext as _
from PetreceriApp.models import User, Party
from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.ModelForm):
    name = fields.CharField(label='Name', max_length=100, required=False)
    username = fields.CharField(label='Username', max_length=20, required=False)
    email = fields.EmailField(label='Email', required=True)
    password = fields.CharField(label='Password', required=True, widget=PasswordInput, max_length=20)
    password2 = fields.CharField(label='Confirm Password', required=True, widget=PasswordInput, max_length=20)

    class Meta:
        model = get_user_model()
        fields = ('name', 'username', 'email', 'password')
    def clean(self):
        self.cleaned_data = super().clean()
        pwd = self.cleaned_data.get('password')
        pwd2 = self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if pwd != pwd2:
            self.add_error('password2', ValidationError(_("Please check again the password you have given. It doesn't "
                                                     "match the first one.")))
        if self.Meta.model.objects.filter(email=email).exists():
            self.add_error('email', ValidationError(_('There is already an account with this email')))
        if self.Meta.model.objects.filter(username=username).exists():
            self.add_error('username', ValidationError(_("This username already exists")))
        try:
            validate_password(pwd)
        except ValidationError as e:
            self.add_error('password', e)

        return self.cleaned_data

    def save(self, **kwargs):
        email = self.cleaned_data.get('email')
        pwd = self.cleaned_data.get('pwd')
        name = None
        username = email

        if len(self.cleaned_data['name']) > 0:
            name = self.cleaned_data['name']
        if len(self.cleaned_data['username']) > 0:
            username = self.cleaned_data['username']
        user = User(email=email, password=pwd, name=name, username=username)
        #user.set_password(pwd)
        user.save()
        authenticate(username=username, password=pwd)
        return user


class CreatePartyForm(forms.ModelForm):

    name = fields.CharField(label='Name', max_length=30)
    location = fields.CharField(label='Location', max_length=30)
    budget_total = fields.IntegerField(label='Budget')
    description = fields.CharField(label='Description', max_length=100, required=False)
    max_nr_people = fields.IntegerField(label='Maximum number of participants')
    date = fields.DateField(label='Date')

    class Meta:
        model = Party
        fields = ['name', 'location', 'budget_total', 'description', 'max_nr_people', 'date']

    def clean(self):
        self.cleaned_data = super().clean()
        name = self.cleaned_data.get('name')
        location = self.cleaned_data.get('location')
        budget = self.cleaned_data.get('budget')
        description = self.cleaned_data.get('description')
        max_nr_people = self.cleaned_data.get('max_nr_people')
        date = self.cleaned_data.get('date')

        return self.cleaned_data


class LoginForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get('username')
        pwd = self.cleaned_data.get('password')
        if username is not None and pwd:
            if not User.objects.filter(username=username).exists():
                self.add_error('username',
                               ValidationError(
                                   _("This username doesn't have an account. Make sure that you provide an existing "
                                     "username.")))
            else:
                self.user_cache = authenticate(
                    self.request, username=username, password=pwd
                )
                if self.user_cache is None:
                    self.add_error('password',
                                       ValidationError(_('Please make sure you enter the correct password. Note that '
                                                         'it may be case-sensitive.')))
        else:
            print('test non-field-error')
            self.add_error(NON_FIELD_ERRORS,
                           ValidationError(_("Please enter a valid %(username)s and password. Note that both fields "
                                             "may be case-sensitive.")))
        return self.cleaned_data

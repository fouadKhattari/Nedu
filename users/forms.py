from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django import forms
from django.forms import ModelForm

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=150)
    Nom = forms.CharField(max_length=100)
    Prenom = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('Prenom' ,'Nom' ,'username', 'email', 'password1', 'password2', )

class UpdateUserForm(forms.ModelForm):
    nom = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    prenom = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['nom','prenom', 'email']

class UpdateProfileForm(forms.ModelForm):
    nom = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'px-3 py-1'}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'px-3 py-1'}))
    prenom = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'px-3 py-1'}))
    age= forms.IntegerField(widget=forms.TextInput(attrs={'class': 'px-3 py-1'}))
    class Meta:
        model = Profile
        fields = ['nom', 'prenom', 'email', 'age']




class ChatMessageForm(ModelForm):
    body = forms.CharField(widget=forms.Textarea(attrs={"class":"forms", "rows":3, "placeholder": "Type message here"}))
    class Meta:
        model = ChatMessage
        fields = ["body",]


class ProfileImage(forms.ModelForm):
    class Meta:
        model = Profile
        fields =  [
            'picture',
        ]
        widgets ={
            'picture': forms.FileInput(attrs = {'class' : 'custom-file-input'}),
        }
    
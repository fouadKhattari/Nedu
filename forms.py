from django import forms
from users.models import *
from quiz.models import Questions

class ChapitreForm(forms.ModelForm):
    class Meta:
        model = Chapitre
        fields =  [
            'titre',
        ]

        
class ParagraphForm(forms.ModelForm):
    class Meta:
        model = Paragraphe
        fields = '__all__'
        widgets ={
            'titre_paragraphe': forms.TextInput(attrs = {'class' : 'form-control'}),
            'contenu': forms.TextInput(attrs = {'class' : 'form-control'}),
            'image': forms.FileInput(attrs = {'class' : 'form-control'}),
        }
        
class VideoForm(forms.ModelForm):
    class Meta:
        model = VideoCours
        fields = '__all__'
        widgets ={
            'titre': forms.TextInput(attrs = {'class' : 'form-control'}),
            'url': forms.TextInput(attrs = {'class' : 'form-control'}),
            'cour': forms.Select(attrs = {'class' : 'form-control'}),
        }
        

class QuizForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields =  [
            'question',
            'option1',
            'option2',
            'option3',
            'option4',
            'reponse',
            'cours',
        ]
        widgets ={
            'question': forms.TextInput(attrs = {'class' : 'form-control'}),
            'option1': forms.TextInput(attrs = {'class' : 'form-control'}),
            'option2': forms.TextInput(attrs = {'class' : 'form-control'}),
            'option3': forms.TextInput(attrs = {'class' : 'form-control'}),
            'option4': forms.TextInput(attrs = {'class' : 'form-control'}),
            'reponse': forms.TextInput(attrs = {'class' : 'form-control'}),
            'cours': forms.Select(attrs = {'class' : 'form-control'}),
        }

class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields =  [
            'titre',
            'photo_cours',
            'disponible',
            'date_creation',
            'domaine',
            'discription',
            'pdf',
        ]
        widgets ={
            'titre': forms.TextInput(attrs = {'class' : 'form-control'}),
            'photo_cours': forms.FileInput(attrs = {'class' : 'form-control'}),
            'date_creation': forms.DateInput(attrs = {'class' : 'form-control'}),
            'domaine': forms.Select(attrs = {'class' : 'form-control'}),
            'discription': forms.TextInput(attrs = {'class' : 'form-control'}),
            'pdf': forms.FileInput(attrs = {'class' : 'form-control'}),
        }

class DomaineForm(forms.ModelForm):
    class Meta:
        model = Domaine
        fields =  [
            'nom',
        ]

        widgets ={
        'nom': forms.TextInput(attrs = {'class' : 'form-control'}),
        }
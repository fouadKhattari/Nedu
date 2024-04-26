from django.shortcuts import render, redirect, get_object_or_404
from users.models import *
from quiz.models import *
from .forms import *
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from array import *


# Create your views here.
@staff_member_required
def admin_profile(request):
    users = User.objects.all()
    staff_users = users.filter(is_staff=True)
    students = users.filter(is_staff=False)
    admin = User.objects.get(username = request.user)
    profile  = Profile.objects.get(user = admin)
    if request.method == 'POST':
        if 'change' in request.POST:
            nom=request.POST['nom']
            prenom=request.POST['prenom']
            email=request.POST['email']
            age=request.POST['age']
            profile.nom = nom
            profile.age = age
            profile.prenom = prenom
            profile.email = email
            profile.save()
            return redirect('adminProfile')
    contexte ={
        'domaine':Domaine.objects.all(),
        'profiles': Profile.objects.all(),
        'cours':Cours.objects.all(),
        'questions':Questions.objects.all(),
        'commentaires':Post.objects.all(),
        'messages':AdminMessage.objects.all(),
        'users':users,
        'admin':admin,
        'profile':profile,
        'titre':'Profile',
        'staffs':staff_users,
        'students':students,
    }
    
    return render(request, 'admin/adminProfile.html',contexte)

@staff_member_required
def admin_cours(request):
    cours = Cours.objects.all()
    admin = User.objects.get(username = request.user)
    profile  = Profile.objects.get(user = admin)
    # for autoSrearch :
    if 'term' in request.GET:
        qs = cours.filter(titre__istartswith = request.GET.get('term'))
        titres = list()
        for cour in qs :
            titres.append(cour.titre)
        return   JsonResponse(titres, safe=False)

    # for search :
    nom_cours = None
    if 'search_name' in request.GET:
        nom_cours = request.GET['search_name']
        if nom_cours :
            cours = cours.filter(titre__icontains=nom_cours)
    
    # pour ajouter cours :
    if 'ajouterCours' in request.POST:
        add_cours = CoursForm(request.POST, request.FILES) 
        if add_cours.is_valid():
            domain = Domaine.objects.get(id=request.POST.get('domaine'))
            domain.counter+= 1
            domain.save()
            add_cours.save()
            return redirect('adminCours')
          
    contexte = {
        'cours':cours,
        'titre':'Espace Cours',
        'coursForm':CoursForm(),
        'admin':admin,
        'profile':profile,
    }
    return render(request, 'admin/adminCours.html',contexte)

@staff_member_required
def admin_etudiant(request):
    students = User.objects.filter(is_staff=False)
    profiles = Profile.objects.all()
    admin = User.objects.get(username = request.user)
    profile  = Profile.objects.get(user = admin)
    
     # for search :
    nom_profile = None
    if 'search_name' in request.GET:
        nom_profile = request.GET['search_name']
        if nom_profile :
            profiles = profiles.filter(nom__icontains=nom_profile) 
         
    # for block cmnt
    if 'blockPost' in request.POST:
        id_etudiant  = request.POST.get('hiddenId')
        user_Et = User.objects.get(id = id_etudiant)
        if user_Et.profile.postBlock :
            user_Et.profile.postBlock = False
        else:
            user_Et.profile.postBlock = True
        user_Et.profile.save()
        return redirect('adminEtudiants')


    contexte = {
        'profiles':profiles,
        'user':User.objects.all(),
        'titre':'Espace Etudiants',
        'admin':admin,
        'profile':profile,
        'students':students,
    }
    return render(request, 'admin/adminEtudiant.html',contexte)

@staff_member_required
def admin_Domains(request):
    domaine = Domaine.objects.all()
    admin = User.objects.get(username = request.user)
    profile  = Profile.objects.get(user = admin)
    # for search :
    nom_domaine = None
    if 'search_name' in request.GET:
        nom_domaine = request.GET['search_name']
        if nom_domaine :
            domaine = domaine.filter(nom__icontains=nom_domaine) 
         
    # pour ajouter domain :
    if request.method == 'POST':
        add_domaine = DomaineForm(request.POST, request.FILES) 
        if add_domaine.is_valid():
            add_domaine.save()

    contexte = {
        'domainForm':DomaineForm(),
        'domaine':domaine,
        'cours':Cours.objects.all(),
        'titre':'Espace Domaines',
        'admin':admin,
        'profile':profile,
    }
    return render(request, 'admin/adminDomains.html',contexte)   

@staff_member_required
def admin_Video(request):
    video = VideoCours.objects.all()
    admin = User.objects.get(username = request.user)
    profile  = Profile.objects.get(user = admin)
    # for search :
    nom_cours = None
    if 'search_name' in request.GET:
        titre_video = request.GET['search_name']
        if titre_video :
            video = video.filter(titre__icontains=titre_video)
         
    # pour ajouter video :
    if request.method == 'POST':
        add_video = VideoForm(request.POST, request.FILES) 
        if add_video.is_valid():
            add_video.save()
            return redirect('.')

    contexte = {
        'VideoForm':VideoForm(),
        'video':video,
        'titre':'Espace videos',
        'admin':admin,
        'profile':profile,
    }
    return render(request, 'admin/adminVideo.html',contexte)  

@staff_member_required
def admin_Forums(request):
    admin = User.objects.get(username = request.user)
    profile  = Profile.objects.get(user = admin)
    postes = Post.objects.all()
    stream  =Stream.objects.get(id=1)
    # for search :
    nom_poste = None
    if 'search_name' in request.GET:
        nom_poste = request.GET['search_name']
        if nom_poste :
            postes = postes.filter(commentaire__icontains=nom_poste)
    if 'room' in request.GET:
        if stream.etat is True:
            stream.etat = False
        else:
            stream.etat = True
        stream.save()
        return redirect('adminForums')     
    contexte = {
        'postes':postes,
        'stream':stream,
        'admin':admin,
        'profile':profile,
        'titre':'Espace Forums'
    }
    return render(request, 'admin/adminForum.html',contexte)

@staff_member_required
def admin_Quiz(request):
    questions = Questions.objects.all()
    admin = User.objects.get(username = request.user)
    profile  = Profile.objects.get(user = admin)
    # pour ajouter domain :
    if request.method == 'POST':
        add_question = QuizForm(request.POST, request.FILES) 
        if add_question.is_valid():
            add_question.save()
    
    # for search :
    question = None
    if 'search_name' in request.GET:
        question = request.GET['search_name']
        if question :
            questions = questions.filter(question__icontains=question) 

    contexte = {
        'quizForm':QuizForm(),
        'questions':questions,
        'profile':profile,
        'admin':admin,
        'titre':'Espace Quiz'
    }
    return render(request, 'admin/adminQuiz.html',contexte)    

@staff_member_required
def post_supprimer(request, id):
    post_delete = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post_delete.delete()
        return redirect('adminForums')

    contexte = {
        'supprimer':'supprimer un post',
        'voulezvous':'voulez-vous supprimer ce poste ?'
    }
    return render(request, 'admin/adminSupprimer.html',contexte)



@staff_member_required
def cours_supprimer(request, id):
    cours_delete = get_object_or_404(Cours, id=id)
    if request.method == 'POST':
        domaine = Domaine.objects.get(nom=cours_delete.domaine)
        domaine.counter -= 1
        for c in cours_delete.chapitres.all():
            for p in c.paragraphes.all():
                p.delete()
            c.delete()
        cours_delete.delete()
        domaine.save()
        return redirect('adminCours')

    contexte = {
        'supprimer':'supprimer le cours',
        'voulezvous':'voulez-vous supprimer ce cours ?'
    }
    return render(request, 'admin/adminSupprimer.html',contexte)


@staff_member_required
def cours_modifier(request, id):
    cours_id = Cours.objects.get(id=id)
    if request.method == 'POST':
        cours_save = CoursForm(request.POST, request.FILES, instance=cours_id)
        if cours_save.is_valid():
            cours_save.save()
            return redirect('adminCours')
    else:
        cours_save = CoursForm(instance=cours_id)

    contexte = {
        'form':cours_save,
        'cours':cours_id,
    }
    return render(request, 'admin/adminModifier.html',contexte)



@staff_member_required
def user_supprimer(request, id):
    user_delete = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_delete.delete()
        return redirect('adminEtudiants')
    
    contexte = {
        'supprimer':'supprimer l\'etudiant',
        'voulezvous':'voulez-vous supprimer cet étudiant ?'
    }
    return render(request, 'admin/adminSupprimer.html',contexte)

@staff_member_required
def domaine_supprimer(request, id):
    domain_delete = get_object_or_404(Domaine, id=id)
    if request.method == 'POST':
        domain_delete.delete()
        return redirect('adminDomains')
    
    contexte = {
        'supprimer':'supprimer le domaine',
        'voulezvous':'voulez-vous supprimer ce domaine ?'
    }
    return render(request, 'admin/adminSupprimer.html',contexte)

@staff_member_required
def video_supprimer(request, id):
    video_delete = get_object_or_404(VideoCours, id=id)
    if request.method == 'POST':
        video_delete.delete()
        return redirect('adminVideo')
    
    contexte = {
        'supprimer':'supprimer le video',
        'voulezvous':'voulez-vous supprimer ce ?'
    }
    return render(request, 'admin/adminSupprimer.html',contexte)

@staff_member_required
def question_supprimer(request, id):
    question_delete = get_object_or_404(Questions, id=id)
    if request.method == 'POST':
        question_delete.delete()
        return redirect('adminQuiz')
    
    contexte = {
        'supprimer':'supprimer la domaine',
        'voulezvous':'voulez-vous supprimer cette video ?'
    }
    return render(request, 'admin/adminSupprimer.html',contexte)

@staff_member_required
def question_modifier(request, id):
    question_id = Questions.objects.get(id=id)
    if request.method == 'POST':
        question_save = QuizForm(request.POST, request.FILES, instance=question_id)
        if question_save.is_valid():
            question_save.save()
            return redirect('adminQuiz')
    else:
        question_save = QuizForm(instance=question_id)

    contexte = {
        'form':question_save,
        'cours':question_id,
    }
    return render(request, 'admin/adminModifier.html',contexte)

@staff_member_required
def video_modifier(request, id):
    video_id = VideoCours.objects.get(id=id)
    if request.method == 'POST':
        video_save = VideoForm(request.POST, request.FILES, instance=video_id)
        if video_save.is_valid():
            video_save.save()
            return redirect('adminVideo')
    else:
        video_save = VideoForm(instance=video_id)

    contexte = {
        'form':video_save,
        'cours':video_id,
    }
    return render(request, 'admin/adminModifier.html',contexte)

@staff_member_required
def admin_messages(request):
    newmessages = AdminMessage.objects.filter(seen=False)
    messages = AdminMessage.objects.all()
    admin = User.objects.get(username = request.user)
    profile  = Profile.objects.get(user = admin)
    if request.method == 'POST':
        if 'confirmer' in request.POST:
            for msg in newmessages:
                msg.seen = True
                msg.save()  
            return redirect('adminMessages') 
        if 'delete' in request.POST:
            AdminMessage.objects.all().delete() 
            return redirect('adminMessages') 
    contexte ={
        'admin':admin,
        'profile':profile,
        'titre' : 'Messages',
        'Newmsgs':newmessages,
        'messages':messages,
    }
    
    return render(request, 'admin/adminMessage.html',contexte)



@staff_member_required
def question_modifier(request, id):
    question_id = Questions.objects.get(id=id)
    if request.method == 'POST':
        question_save = QuizForm(request.POST, request.FILES, instance=question_id)
        if question_save.is_valid():
            question_save.save()
            return redirect('adminQuiz')
    else:
        question_save = QuizForm(instance=question_id)

    contexte = {
        'form':question_save,
        'cours':question_id,
    }
    return render(request, 'admin/adminModifier.html',contexte)

def ajouterchapitre(request, id):
    cour = Cours.objects.get(id=id)
    form  = ChapitreForm()
    if request.method == 'POST':
        if 'ajouter' in request.POST:
            form = ChapitreForm(request.POST)
            if form.is_valid():
                titre = form.cleaned_data['titre']
                chapitre =cour.chapitres.create(titre=titre)
                chapitre.save()
                id_chapitre = chapitre.id
                return render(request, 'admin/infoChapitre.html', {'chapitre':id_chapitre, 'cour':cour}) 
    contexte = {
        'form':form,
        'cour': cour,
    }
    return render(request, 'admin/adminAjouterchapitre.html', contexte)


@staff_member_required
def ajouterPara(request, id):
    form = ParagraphForm()
    if request.method == 'POST':
        paragraphe = ParagraphForm(request.POST, request.FILES)
        if paragraphe.is_valid():
            chapitre = Chapitre.objects.get(id=id)
            image = paragraphe.cleaned_data['image']
            titre = paragraphe.cleaned_data['titre_paragraphe']
            contenu = paragraphe.cleaned_data['contenu']
            have = paragraphe.cleaned_data['have_image']
            chapitre = chapitre.paragraphes.create(titre_paragraphe=titre, image=image, contenu=contenu, have_image=have )
            chapitre.save()
            
            
    contexte = {'form':form}
    return render(request, 'admin/ajouterParagraphe.html', contexte)


     

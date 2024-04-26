from django.http import JsonResponse
from .models import *
from django.shortcuts import render, redirect
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .forms import *
from django.contrib.auth.forms import PasswordChangeForm
from .forms import SignUpForm
from .tokens import account_activation_token
from django.db.models import Q
import json


def index(request):
    user = request.user
    search =  Cours.objects.all()
    # for autoSrearch :
    if 'term' in request.GET:
        qs = search.filter(titre__istartswith = request.GET.get('term'))
        titres = list()
        for cour in qs :
            titres.append(cour.titre)
        return   JsonResponse(titres, safe=False)
    # for serch :
    nom_cours = None
    if 'search_name' in request.GET:
        nom_cours = request.GET['search_name']
        if nom_cours :
            search = search.filter(titre__icontains=nom_cours)

    Did = request.GET.get('domaines')
    if Did :
        search = search.filter(domaine = Did)
    else:
        search = search
    domaines = Domaine.objects.all()
    doaminesID = []
    for d in domaines :
        doaminesID.append(d.id)

    x = {
        'css' : '/static/css/accueil.css',
        'cours' : search,
        'domaines': domaines,
        'user':user,
        'doaminesID':doaminesID,
        }
    return render(request, 'internaute/index.html', x)

def cours(request):
    user = request.user
    cour = Cours.objects.all()
    domaines = Domaine.objects.all()
    nom = None
    if 'cours_nom' in request.GET:
        nom = request.GET['cours_nom']
        if nom :
            cour = cour.filter(titre__icontains=nom)

    Did = request.GET.get('domaines')
    if Did :
        cour = cour.filter(domaine = Did)
    else:
        cour = cour
    x = {
        'css' : '/static/css/cours.css',
        'cours' : cour,
        'domaines': domaines,
        'user':user,
        }
    return render(request, 'internaute/cours.html', x)

def about(request):
    domains = Domaine.objects.all()
    x = {
        'css' : '/static/css/about.css',
        'domaines':domains,

        }
    return render(request, 'internaute/about.html',x )

def activate(request, uidb64, token):
    try:
        uid = force_str (urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.signup_confirmation = True
        user.save()
        friend = Friend()
        friend.profile = user.profile
        friend.save()
        login(request, user)
        return redirect('index')
    else:
        return render(request, 'internaute/activation_invalid.html')

def activation_sent_view(request):
    return render(request, 'internaute/activation_sent.html')



def signup_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method  == 'POST':
          form = SignUpForm(request.POST)
          if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            nom = form.cleaned_data.get('Nom')
            prenom = form.cleaned_data.get('Prenom')
            email = form.cleaned_data.get('email')
            user.profile.nom = nom
            user.profile.prenom = prenom
            user.profile.email = email
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('internaute/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            user.email_user(subject, message)
            email = EmailMessage(
                subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'internaute/activation_sent.html')
        else:
            form = SignUpForm()
    return render(request, 'internaute/signup.html', {'form': form})


def logoutUser(request):
    profile = request.user.profile
    profile.etat = False
    profile.save()
    logout(request)
    return redirect('login')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if (user is not None and user.is_active == True):
                login(request, user)
                if  user.is_staff:
                 return redirect('adminProfile')
                return redirect('profile')
            else:
               messages.info(request, 'Username or password incorrect')
    return render(request, 'internaute/login.html')

@login_required(login_url="login")
def profile(request):
    form = PasswordChangeForm(request.user)
    etudiant = User.objects.get(username = request.user)
    profile  = Profile.objects.get(user = etudiant)
    msg = ''
    updatePicture = ProfileImage()
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
            return redirect('profile')
        if 'ContactAdmin' in request.POST:
            body=request.POST['body']
            message = AdminMessage(body=body, msg_sender=request.user)
            message.save()
            if body.find('Stream') or body.find('reunion') or body.find('viedo') or body.find('call vedio') or body.find('room'):
                s = Stream.objects.get(id=1)
                s.etat = True
                s.save()
                msg = 'The Stream is open'
            else:
                msg = 'votre message est envoyé'
            return redirect('profile')
        else:
            msg=''

        if 'changePicture' in request.POST:
            updatePicture = ProfileImage(request.POST, request.FILES, instance=request.user.profile)
            if updatePicture.is_valid():
                profile=updatePicture.save(commit=False)
                profile.user = request.user
                profile.save()
                return redirect('profile')
            else:
                 return redirect('profile')

    profile.etat = True
    profile.save()
    contexte = {
        'form':form,
        'css':'/static/css/etudiant.css',
        'user':etudiant,
        'profile':profile,
        'domaines': Domaine.objects.all(),
        'msg':msg,
        'formPicure':updatePicture,
    }
    return render(request, 'users/profile.html', contexte)

@login_required(login_url="login")
def Contenu(request, pk):
    cour = Cours.objects.get(id=pk)
    etudiant = User.objects.get(username = request.user)
    posts = Post.objects.filter(cour=cour)
    if request.method == 'POST':
        if 'commentaire' in request.POST:
            content=request.POST['commentaire']
            if len(content)>0:
                comment = Post(commentaire=content, writer=etudiant, cour=cour)
                comment.save()
                return redirect('.')
            else:
                return redirect('.')

    # for like
    user = request.user
    if request.method == 'POST':
        if 'like' in request.POST:
            cour_obj = Cours.objects.get(id=pk)
            if user in cour_obj.liked.all():
               cour_obj.liked.remove(user)
            else:
               cour_obj.liked.add(user)
            return redirect('.')

        like, created = Like.objects.get_or_create(user=user, cour_id=pk)
        like.save()
    contexte = {
        'css':'/static/css/etudiantCours.css',
        'cour':cour,
        'posts':posts,
        'domaines': Domaine.objects.all(),
        'user':etudiant,
    }
    return render(request, 'users/contenu-cour.html', contexte)



@login_required(login_url="login")
def pdfpage(request, pk):
    user = request.user
    cour = Cours.objects.get(id=pk)
    contexte = {
        'css':'/static/css/etudiantCours.css',
        'cour':cour,
        'user':user,
    }
    return render(request, 'users/pdfpage.html', contexte)

@login_required(login_url="login")
def videoCours(request, pk):
    user = request.user
    cours = Cours.objects.get(id=pk)
    videos = VideoCours.objects.filter(cour=cours)
    contexte = {
        'css':'/static/css/etudiantCours.css',
        'videos':videos,
        'user':user,
    }
    return render(request, 'users/videoCours.html', contexte)



@login_required(login_url='login')
def room(request):
    stream  =Stream.objects.get(id=1)
    user = request.user
    domaines = Domaine.objects.all()
    users = User.objects.all()
    filecss ='/static/css/room.css'
    contexte = {'css':filecss, 'users':users, 'domaines':domaines, 'user':user, 'stream':stream }
    return render(request, 'users/room.html', contexte)


@login_required(login_url="login")
def chat(request):
    domaines = Domaine.objects.all()
    user = request.user

    if(user.profile.isFriend == False):
        user.profile.isFriend = True
        friend = Friend()
        friend.profile = user.profile
        friend.save()
    user = user.profile
    users = User.objects.filter(is_superuser=False, is_staff=False)
    users = users.filter(~Q(username = request.user.username) )
    # for serch :
    nom_etudiant = None
    if 'search_name' in request.GET:
        nom_etudiant = request.GET['search_name']
        if nom_etudiant :
            users = users.filter(username__icontains=nom_etudiant)

    if request.method == 'POST':
        if 'addfriend' in request.POST:
            friend_id  = request.POST['friendId']
            userF = User.objects.get(id = friend_id)
            friend = Friend.objects.filter(profile=userF.profile)
            user.friends.add(*friend)

    friends = user.friends.all()
    context = {"user": user, "friends": friends, 'domaines':domaines, 'users':users}
    return render(request, "chatapp/index.html", context)



@login_required(login_url="login")
def detail(request,pk):
    domaines = Domaine.objects.all()
    user_rec = User.objects.get(id=pk)
    profile_rec = Profile.objects.get(user=user_rec)
    friend = Friend.objects.get(profile=profile_rec)
    user = request.user.profile
    profile = profile_rec
    chats = ChatMessage.objects.all()
    rec_chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user, seen=False)
    rec_chats.update(seen=True)
    form = ChatMessageForm()
    if request.method == "POST":
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.msg_sender = user
            chat_message.msg_receiver = profile
            chat_message.save()
            return redirect("detail", pk=friend.profile.id)
    context = {"friend": friend, "form": form, "user":user,
               "profile":profile, "chats": chats, "num": rec_chats.count(), 'domaines':domaines}
    return render(request, "chatapp/detail.html", context)


@login_required(login_url="login")
def sentMessages(request, pk):
    user_rec = User.objects.get(id=pk)
    user = request.user.profile
    profile = user_rec.profile
    data = json.loads(request.body)
    new_chat = data["msg"]
    new_chat_message = ChatMessage.objects.create(body=new_chat, msg_sender=user, msg_receiver=profile, seen=False )
    return JsonResponse(new_chat_message.body, safe=False)

@login_required(login_url="login")
def receivedMessages(request, pk):
    user = request.user.profile
    user_rec = User.objects.get(id=pk)
    profile_rec = Profile.objects.get(user=user_rec)
    profile = profile_rec
    arr = []
    chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user)
    for chat in chats:
        arr.append(chat.body)
    return JsonResponse(arr, safe=False)

@login_required(login_url="login")
def chatNotification(request):
    user = request.user.profile
    friends = user.friends.all()
    user = request.user.profile
    arr = []
    for friend in friends:
        user_rec = User.objects.get(id=friend.profile.user.id)
        profile = Profile.objects.get(user=user_rec)
        chats = ChatMessage.objects.filter(msg_sender=profile, msg_receiver=user, seen=False)
        arr.append(chats.count())
    return JsonResponse(arr, safe=False)

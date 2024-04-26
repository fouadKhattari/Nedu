from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q





class Profile(models.Model):
    nom = models.CharField(max_length=100, null=True, blank=True)
    prenom = models.CharField(max_length=100, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    email = models.CharField(max_length=200,  blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    signup_confirmation = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='users_picture', default='users_picture/default.png' )
    friends = models.ManyToManyField('Friend', related_name = "my_friends")
    etat = models.BooleanField(default=False, blank=True)
    isFriend=models.BooleanField(default=True)
    postBlock = models.BooleanField(default=False, blank=True)
    ville = models.CharField(blank=True, max_length=200)
    def __str__(self):
        return self.nom



class Domaine(models.Model):
    nom = models.CharField(max_length=50)
    counter = models.IntegerField(default=0)
    def __str__(self) :
       return self.nom


class Paragraphe(models.Model):
    titre_paragraphe = models.TextField(null=True, blank=True)
    contenu = models.TextField()
    have_image = models.BooleanField(default=False)
    image = models.ImageField(upload_to='photos', null=True, blank=True)
    def __str__(self) :
       return self.contenu

class Chapitre(models.Model):
    titre = models.CharField(max_length=50)
    paragraphes = models.ManyToManyField(Paragraphe, related_name='choices', null=True, blank=True)


class Cours(models.Model):
    titre = models.CharField(max_length=50)
    photo_cours = models.ImageField(upload_to='photos', null=True, blank=True)
    disponible = models.BooleanField(default=True)
    date_creation =models.DateField(null=True, blank=True)
    domaine =models.ForeignKey(Domaine, on_delete=models.PROTECT, null=True, blank=True)
    chapitres = models.ManyToManyField(Chapitre, related_name='choices', null=True, blank=True)
    discription = models.TextField(null=True, blank=True)
    pdf = models.FileField(upload_to='PDFs',null=True, blank=True)
    type = models.CharField(max_length=50, null=True, blank=True)
    counter = models.IntegerField(default=0)
    liked = models.ManyToManyField(User, default=None, null=True, blank=True, related_name='liked')
    def __str__(self) :
       return self.titre

    @property
    def num_likes(self):
        return self.liked.all().count()

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"



LIKE_CHOICES = (
    ('Like','like'), ('Unlike','unlike')
)
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cour = models.ForeignKey(Cours, on_delete=models.CASCADE)
    value = models.CharField(max_length=15, choices=LIKE_CHOICES, default='Like')

    def __str__(self):
        return str(self.cour)


class Post(models.Model):
    commentaire = models.TextField(null=True, blank=True)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    cour = models.ForeignKey(Cours, on_delete=models.CASCADE)

class VideoCours(models.Model):
    titre = models.CharField(max_length=50, blank=True, null=True)
    url = models.CharField(max_length=100)
    cour = models.ForeignKey(Cours, on_delete=models.CASCADE, blank=True, null=True)

# chat
class Friend(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return self.profile.nom

class ChatMessage(models.Model):
    body = models.TextField()
    msg_sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_sender")
    msg_receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="msg_receiver")
    seen = models.BooleanField(default=False)
    def __str__(self):
        return self.body

class AdminMessage(models.Model):
    body = models.TextField()
    msg_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_sender")
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.body


class Stream(models.Model):
    etat = models.BooleanField(blank=True)
    def __str__(self):
        return self.etat

from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Domaine)
admin.site.register(Cours)
admin.site.register(Paragraphe)
admin.site.register(Profile)
admin.site.register(Chapitre)
admin.site.register(Like)
admin.site.register(Post)
admin.site.register(Friend)
admin.site.register(ChatMessage)
admin.site.register(AdminMessage)
admin.site.register(VideoCours)


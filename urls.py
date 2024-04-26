from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # cote admin information et gestion des messages
    path('admin-profile/', views.admin_profile, name='adminProfile'),
    path('admin-messages/', views.admin_messages, name='adminMessages'),

    # les lien des cours
    path('admin-cours/', views.admin_cours, name='adminCours'),
    path('cours-supprimer/<int:id>', views.cours_supprimer, name='coursSupprimer'),
    path('cours-modifier/<int:id>', views.cours_modifier, name='coursModifier'),
    path('ajouterChapitre/<int:id>', views.ajouterchapitre, name='ajouterChapitre'),
    path('ajouterParagraphe/<int:id>', views.ajouterPara, name='ajouterPara'),


    #les lien des users
    path('admin-etudiants/', views.admin_etudiant, name='adminEtudiants'),
    path('user-supprimer/<int:id>', views.user_supprimer, name='userSupprimer'),
    
    # les lien des domains
    path('admin-domains/', views.admin_Domains, name='adminDomains'),
    path('domaine-supprimer/<int:id>', views.domaine_supprimer, name='domaineSupprimer'),

    # forum and posts
    path('admin-forums/', views.admin_Forums, name='adminForums'),
    path('post-supprimer/<int:id>', views.post_supprimer, name='postSupprimer'),
    
    # Quiz 
    path('admin-quiz/', views.admin_Quiz, name='adminQuiz'),
    path('question-supprimer/<int:id>', views.question_supprimer, name='questionSupprimer'),
    path('question-modifier/<int:id>', views.question_modifier, name='questionModifier'),

    # videos des cours
    path('admin-video/', views.admin_Video, name='adminVideo'),
    path('video-supprimer/<int:id>', views.video_supprimer, name='videoSupprimer'),
    path('video-modifier/<int:id>', views.video_modifier, name='videoModifier'),

    

   

    




]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
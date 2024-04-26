from django.urls import path, reverse_lazy
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView


urlpatterns = [

    path('', views.index, name='index'),
    path('cours/', views.cours, name='cours'),
    path('A-prpos/', views.about, name='about'),
    path('signup/', views.signup_view, name='signup'),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('login/', views.login_page, name='login'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logoutUser, name='logout'),
    path('contenu/<str:pk>/', views.Contenu, name='contenu'),
    path('pdfpage/<str:pk>/', views.pdfpage, name='pdfpage'),
    path('videoCours/<str:pk>/', views.videoCours, name='videoCours'),
    path('chat/', views.chat, name='chat'),
    path('friend/<str:pk>', views.detail, name="detail"),
    path('sent_msg/<str:pk>', views.sentMessages, name = "sent_msg"),
    path('rec_msg/<str:pk>', views.receivedMessages, name = "rec_msg"),
    path('notification', views.chatNotification, name = "notification"),
    path('room/', views.room, name='room'),


    path('change_password/', PasswordChangeView.as_view(template_name = 'users/change_password.html', success_url = reverse_lazy('password_change_done')
    ) , name='password_change'),
    path('change_password/done/',
         PasswordChangeDoneView.as_view( template_name = 'users/change_password_done.html') , name='password_change_done')


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
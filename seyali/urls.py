from django.urls import path
from .views import content_list, content_upload, content_delete, register, home_redirect, content_edit, quiz_list
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .quiz import take_quiz
#from seyali.views import quiz_list, quiz_detail, quiz_create, quiz_edit, quiz_delete

urlpatterns = [
    path('', home_redirect, name='home_redirect'),
    path('content/', content_list, name='content_list'),
    path('upload/', content_upload, name='content_upload'),
    path('delete/<int:content_id>/', content_delete, name='content_delete'),
    path('edit/<int:content_id>/', content_edit, name='content_edit'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', register, name='register'),
    path('quiz/<int:quiz_id>/', take_quiz, name='take_quiz'),
    path('quizzes/', quiz_list, name='quiz_list'),
    #path('quizzes/<int:quiz_id>/', quiz_detail, name='quiz_detail'),
    #path('quizzes/create/', quiz_create, name='quiz_create'),
    #path('quizzes/<int:quiz_id>/edit/', quiz_edit, name='quiz_edit'),
    #path('quizzes/<int:quiz_id>/delete/', quiz_delete, name='quiz_delete'),
]

# Add these lines to serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
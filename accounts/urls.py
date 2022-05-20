from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', views.SignInView.as_view(), name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('check-username/', views.check_username, name='check-username'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add-tag/<int:pk>/', views.add_tag, name='add-tag'),
    path('delete-tag/<int:pk>/', views.delete_tag, name='delete-tag'),
]

from django.urls import path
from . import views
urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('profile', views.profile, name='profile'),
    path('change-password', views.changePassword, name='changePassword'),
    path('followers', views.followers, name='followers'),
    path('following', views.following, name='following'),
]

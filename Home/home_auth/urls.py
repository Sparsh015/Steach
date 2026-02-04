from django.contrib import admin
from django.urls import path, include
from . views import *

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('reset_password/<str:token>', reset_password_view, name='reset_password'),
    path('forgot_password/', forgot_password_view, name='forgot-password'),

]

from django.urls import path
from django.urls import path
from .import views
urlpatterns=[
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('verify/<slug:token>',views.verify,name='verify'),
    path('logout',views.logout,name='logout'),
]
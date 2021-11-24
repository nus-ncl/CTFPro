from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    
    path('login.html/', views.login, name='login'),
    
    path("register.html/", views.register_request, name="register"),
    
    path('index.html/', views.index, name='index'),
    
    path('challenges.html/', views.challenges, name='challenges'),

    
    path('components.html/', views.components, name='components'),

    
    path('dashboard.html/', views.dashboard, name='dashboard'),

    
    path('landpage.html/', views.landpage, name='landpage'),

    
    path('monitor.html/', views.monitor, name='monitor'),

    
    path('stats.html/', views.stats, name='stats'),

    
]


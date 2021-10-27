from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html/', views.index, name='index'),
    
    path('challenges.html/', views.challenges, name='challenges'),

    
    path('components.html/', views.components, name='components'),

    
    path('dashboard.html/', views.dashboard, name='dashboard'),

    
    path('landpage.html/', views.landpage, name='landpage'),

    
    path('monitor.html/', views.monitor, name='monitor'),

    
    path('stats.html/', views.stats, name='stats'),

    
]


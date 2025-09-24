from ipo import views
from django.urls import path

urlpatterns = [
    path('', views.ipo, name='ipo'),
    path('upcomming/', views.upcomming, name='upcomming')
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('items/', views.item_list, name='item_list'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),
    path('items/create/', views.item_create, name='item_create'),
    path('items/<int:pk>/edit/', views.item_edit, name='item_edit'),
    path('items/<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('items/<int:item_pk>/exchange/', views.create_exchange_proposal, name='create_exchange_proposal'),
    path('proposals/', views.proposal_list, name='proposal_list'),
    path('proposals/<int:pk>/', views.proposal_detail, name='proposal_detail'),
    path('proposals/<int:pk>/accept/', views.accept_proposal, name='accept_proposal'),
    path('proposals/<int:pk>/reject/', views.reject_proposal, name='reject_proposal'),
    path('proposals/<int:pk>/complete/', views.complete_exchange, name='complete_exchange'),
    path('profile/edit/', views.profile, name='profile_edit'),
    path('profile/', views.profile, name='profile'),
] 
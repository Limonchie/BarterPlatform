from django.urls import path
from . import views

urlpatterns = [
    path('ads/create/', views.create_ad, name='create_ad'),
    path('ads/<int:ad_id>/edit/', views.edit_ad, name='edit_ad'),
    path('ads/<int:ad_id>/delete/', views.delete_ad, name='delete_ad'),
    path('ads/', views.ad_list, name='ad_list'),
    path('ads/<int:ad_id>/', views.ad_detail, name='ad_detail'),

    path('proposals/', views.proposals_list, name='proposals_list'),
    path('proposals/create/<int:ad_sender_id>/', views.create_proposal, name='create_proposal'),
    path('proposals/<int:proposal_id>/<str:new_status>/',
         views.update_proposal_status, name='update_proposal_status'),
]
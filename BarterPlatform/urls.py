from django.contrib import admin
from django.urls import path, include
from ads import views as ads_views
from BarterPlatform import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ads/', include([
        path('', ads_views.ad_list, name='ad_list'),
        path('create/', ads_views.create_ad, name='create_ad'),
        path('<int:ad_id>/', ads_views.ad_detail, name='ad_detail'),
        path('<int:ad_id>/edit/', ads_views.edit_ad, name='edit_ad'),
        path('<int:ad_id>/delete/', ads_views.delete_ad, name='delete_ad'),
    ])),
    path('proposals/', include([
        path('', ads_views.proposals_list, name='proposals_list'),
        path('create/<int:ad_sender_id>/', ads_views.create_proposal, name='create_proposal'),
        path('<int:proposal_id>/<str:new_status>/',
             ads_views.update_proposal_status, name='update_proposal_status'),
    ])),
    path('users/', include('users.urls')),
    path('', views.home, name='home'),
path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
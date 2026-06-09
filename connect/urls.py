from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('explore/', views.explore, name='explore'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/<int:user_id>/', views.profile_detail, name='profile_detail'),
    path('connect/<int:user_id>/', views.send_connection, name='send_connection'),
    path('connections/', views.connections, name='connections'),
    path('connection/<int:connection_id>/<str:action>/', views.respond_connection, name='respond_connection'),
    path('messages/', views.inbox, name='inbox'),
    path('messages/<int:user_id>/', views.chat, name='chat'),
    path('reveal-contact/<int:user_id>/', views.reveal_contact, name='reveal_contact'),
    path('post/create/', views.create_post, name='create_post'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

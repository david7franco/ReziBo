from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView
from . import views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('text-entry/', views.text_entry, name='text_entry'),
    path('trello/', views.trello_board, name='trello_board'),
    path('move_task/', views.move_task, name='move_task'),
    path('login/', views.login_view, name='login'),
    path('residentDashboard/', views.resident_dashboard, name= 'resident_dashboard'),
    path('createTicket/', views.create_ticket, name= 'create_ticket'),
    path('chat/<str:Open_Ticket>/', views.chat_room, name='chat_room'),
    path('chat/<str:Open_Ticket>/messages/', views.get_messages, name='get_messages'),

]
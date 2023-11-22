from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView
from . import views
from .views import task_chat

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path('trello/', views.trello_board, name='trello_board'),
    path('move_task/', views.move_task, name='move_task'),
    path('login/', views.login_view, name='login'),
    path('residentDashboard/', views.resident_dashboard, name= 'resident_dashboard'),
    path('profile-view/', views.profile_view, name='profile-view'),
    path('createTicket/', views.create_ticket, name= 'create_ticket'),
    #path('chat/', views.chat_room, name='chatroom'),
    #path('chat/<str:Open_Ticket>/', views.chat_room, name='chat_room'),
    #path('chat/<str:Open_Ticket>/messages/', views.get_messages, name='get_messages'),
    path('task/<int:task_id>/chat/', task_chat, name='task_chat'),
    path('chat/messages/<int:task_id>/', views.fetch_messages, name='chat_message_fetch'),
    path('chat/send/<int:task_id>/', views.send_message, name='chat_message_send'),
    path('openTicket/<int:task_id>/', views.open_ticket, name='open_ticket'),
]
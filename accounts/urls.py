from django.urls import path
from django.contrib.auth import views as auth_views
from .views import SignUpView
from . import views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('text-entry/', views.text_entry, name='text_entry'),
    path('text-display/', views.text_display, name='text_display'),
    path('trello/', views.trello_board, name='trello_board'),
    path('move_task/', views.move_task, name='move_task'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
from django.urls import path

from .views import SignUpView
from . import views

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('text-entry/', views.text_entry, name='text_entry'),
    path('text-display/', views.text_display, name='text_display'),
    path('trello/', views.trello_board, name='trello_board')

]
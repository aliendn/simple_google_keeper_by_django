from django.urls import path
from .views import register_user, logout, login_user, note_creator, shownotes, edit_notes


app_name = 'user'

urlpatterns = [
    path('register/', register_user, name="register"),
    path('logout/', logout, name="logout"),
    path('login/',login_user, name='login'),
    path('create/', note_creator, name='note_creating'),
    path('profile/', shownotes, name='profile'),
    path('edit_notes/<int:id>', edit_notes, name='edit_notes')
]

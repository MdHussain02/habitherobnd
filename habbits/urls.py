from django.urls import path
from .views import *


urlpatterns = [
    path('login', CustomLoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('profile', UserProfileView.as_view(), name='user_profile'),
    path('habits-list', HabitListView.as_view(), name='habit_list'),
    path('habits/create', HabitView.as_view(), name='create_habit'),
    path('habits/<int:habit_id>', HabitView.as_view(), name='habit_detail'),
    path('profile/choices', ProfileChoicesView.as_view(), name='profile-choices'),

]
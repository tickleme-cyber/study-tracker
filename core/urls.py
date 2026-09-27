from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('', views.landing_view, name='landing'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Core Features
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('subjects/', views.subjects_view, name='subjects'),
    path('subjects/<int:pk>/delete/', views.delete_subject_view, name='delete_subject'),
    path('focus-timer/', views.focus_timer_view, name='focus_timer'),
    path('log-session/', views.log_session_view, name='log_session'),
    path('goals/', views.goals_view, name='goals'),
    path('goals/<int:pk>/toggle/', views.toggle_goal_view, name='toggle_goal'),
    path('goals/<int:pk>/delete/', views.delete_goal_view, name='delete_goal'),
    path('flashcards/', views.flashcards_view, name='flashcards'),
    path('flashcards/deck/<int:deck_id>/', views.deck_detail_view, name='deck_detail'),
    path('flashcards/card/<int:pk>/delete/', views.delete_card_view, name='delete_card'),
    path('flashcards/deck/<int:pk>/delete/', views.delete_deck_view, name='delete_deck'),
    path('habits/toggle/<int:habit_id>/', views.toggle_habit_view, name='toggle_habit'),
    path('habits/delete/<int:pk>/', views.delete_habit_view, name='delete_habit'),
    path('mood/', views.mood_view, name='mood'),
    path('doubts/', views.doubts_view, name='doubts'),
    path('doubts/<int:pk>/toggle/', views.toggle_doubt_view, name='toggle_doubt'),
    path('doubts/<int:pk>/delete/', views.delete_doubt_view, name='delete_doubt'),
    path('update-exam-date/', views.update_exam_date_view, name='update_exam_date'),
]

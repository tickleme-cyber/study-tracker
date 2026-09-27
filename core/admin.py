from django.contrib import admin
from .models import (
    Subject, StudySession, Goal,
    FlashcardDeck, Flashcard,
    Habit, HabitLog, MoodEntry,
    Doubt, Achievement, UserProfile,
)

admin.site.register(Subject)
admin.site.register(StudySession)
admin.site.register(Goal)
admin.site.register(FlashcardDeck)
admin.site.register(Flashcard)
admin.site.register(Habit)
admin.site.register(HabitLog)
admin.site.register(MoodEntry)
admin.site.register(Doubt)
admin.site.register(Achievement)
admin.site.register(UserProfile)

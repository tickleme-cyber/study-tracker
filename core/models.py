from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Subject(models.Model):
    """A subject/course being studied."""
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default='#7c3aed', help_text='Hex color code')
    icon = models.CharField(max_length=50, default='📚')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class StudySession(models.Model):
    """A study session with start/end times."""
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='sessions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-start_time']


class Goal(models.Model):
    """A study goal with progress tracking."""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='goals')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    target_hours = models.FloatField(default=10.0)
    completed_hours = models.FloatField(default=0.0)
    deadline = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def progress_percent(self):
        if self.target_hours == 0:
            return 100
        return min(100, int((self.completed_hours / self.target_hours) * 100))

    class Meta:
        ordering = ['-created_at']


class FlashcardDeck(models.Model):
    """A deck of flashcards."""
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='decks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcard_decks')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def card_count(self):
        return self.cards.count()


class Flashcard(models.Model):
    """A single flashcard with front/back content."""
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    deck = models.ForeignKey(FlashcardDeck, on_delete=models.CASCADE, related_name='cards')
    front = models.TextField()
    back = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    last_reviewed = models.DateTimeField(null=True, blank=True)
    times_reviewed = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.front[:50]}..."


class Habit(models.Model):
    """A daily study habit to track."""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    streak_count = models.PositiveIntegerField(default=0)
    best_streak = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class HabitLog(models.Model):
    """Log of habit completion per day."""
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField(default=timezone.now)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['habit', 'date']
        ordering = ['-date']

    def __str__(self):
        status = '✅' if self.completed else '❌'
        return f"{self.habit.name} - {self.date} {status}"


class MoodEntry(models.Model):
    """Daily mood tracking."""
    MOOD_CHOICES = [
        (1, '😞 Bad'),
        (2, '😐 Okay'),
        (3, '😊 Good'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mood_entries')
    date = models.DateField(default=timezone.now)
    mood_score = models.IntegerField(choices=MOOD_CHOICES)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} - Mood: {self.mood_score}"


class Doubt(models.Model):
    """A study doubt/question."""
    question = models.TextField()
    answer = models.TextField(blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True, related_name='doubts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doubts')
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:80]

    class Meta:
        ordering = ['-created_at']


class Achievement(models.Model):
    """Badges and achievements."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='🏆')
    criteria = models.TextField(help_text='Description of how to earn this achievement')
    points = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """Extended user profile for study tracking."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    total_study_minutes = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    best_streak = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    exam_date = models.DateField(null=True, blank=True)
    chapters_remaining = models.PositiveIntegerField(default=0)
    achievements = models.ManyToManyField(Achievement, blank=True, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile: {self.user.username}"

    @property
    def total_study_hours(self):
        return round(self.total_study_minutes / 60, 1)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import date, timedelta
import json

from .models import (
    Subject, StudySession, Goal, FlashcardDeck, Flashcard,
    Habit, HabitLog, MoodEntry, Doubt, UserProfile
)
from .forms import (
    RegisterForm, SubjectForm, GoalForm, FlashcardForm,
    FlashcardDeckForm, HabitForm, DoubtForm, StudySessionForm
)


def landing_page(request):
    """Landing page with hero, features, and live demo sections."""
    return render(request, 'landing.html')


def register_view(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """User login."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    from django.contrib.auth.forms import AuthenticationForm
    from django.contrib.auth import authenticate
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            error = 'Invalid username or password'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    """User logout."""
    logout(request)
    return redirect('landing')


@login_required
def dashboard(request):
    """Main user dashboard with study stats and recent activity."""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    subjects = Subject.objects.filter(user=request.user)
    recent_sessions = StudySession.objects.filter(user=request.user)[:5]
    goals = Goal.objects.filter(user=request.user, completed=False)[:5]
    habits = Habit.objects.filter(user=request.user)
    today = date.today()

    # Get today's habit logs
    for habit in habits:
        habit.done_today = HabitLog.objects.filter(
            habit=habit, date=today, completed=True
        ).exists()

    # Calculate stats
    total_sessions = StudySession.objects.filter(user=request.user).count()
    total_minutes = sum(s.duration_minutes for s in StudySession.objects.filter(user=request.user))
    total_hours = round(total_minutes / 60, 1)
    completed_goals = Goal.objects.filter(user=request.user, completed=True).count()

    # Streak calendar data (last 28 days)
    streak_data = []
    for i in range(27, -1, -1):
        d = today - timedelta(days=i)
        has_session = StudySession.objects.filter(user=request.user, start_time__date=d).exists()
        streak_data.append({'date': d, 'active': has_session})

    context = {
        'profile': profile,
        'subjects': subjects,
        'recent_sessions': recent_sessions,
        'goals': goals,
        'habits': habits,
        'total_sessions': total_sessions,
        'total_hours': total_hours,
        'completed_goals': completed_goals,
        'streak_data': streak_data,
    }
    return render(request, 'dashboard.html', context)


@login_required
def flashcards_view(request):
    """Flashcard study interface."""
    decks = FlashcardDeck.objects.filter(user=request.user)
    deck_id = request.GET.get('deck')
    cards = []
    current_deck = None

    if deck_id:
        current_deck = get_object_or_404(FlashcardDeck, id=deck_id, user=request.user)
        cards = list(current_deck.cards.values('id', 'front', 'back', 'difficulty'))

    if request.method == 'POST':
        if 'new_deck' in request.POST:
            deck_form = FlashcardDeckForm(request.POST)
            if deck_form.is_valid():
                deck = deck_form.save(commit=False)
                deck.user = request.user
                deck.save()
                return redirect(f'/flashcards/?deck={deck.id}')
        elif 'new_card' in request.POST:
            card_form = FlashcardForm(request.POST)
            if card_form.is_valid():
                card = card_form.save(commit=False)
                card.deck_id = request.POST.get('deck_id')
                card.save()
                return redirect(f'/flashcards/?deck={card.deck_id}')

    deck_form = FlashcardDeckForm()
    deck_form.fields['subject'].queryset = Subject.objects.filter(user=request.user)
    card_form = FlashcardForm()

    context = {
        'decks': decks,
        'current_deck': current_deck,
        'cards_json': json.dumps(cards),
        'deck_form': deck_form,
        'card_form': card_form,
    }
    return render(request, 'flashcards.html', context)


@login_required
def focus_timer_view(request):
    """Pomodoro focus timer."""
    subjects = Subject.objects.filter(user=request.user)
    return render(request, 'focus_timer.html', {'subjects': subjects})


@login_required
def goals_view(request):
    """Goals management."""
    goals = Goal.objects.filter(user=request.user)
    if request.method == 'POST':
        form = GoalForm(request.POST)
        form.fields['subject'].queryset = Subject.objects.filter(user=request.user)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goals')
    else:
        form = GoalForm()
        form.fields['subject'].queryset = Subject.objects.filter(user=request.user)

    return render(request, 'goals.html', {'goals': goals, 'form': form})


@login_required
def subjects_view(request):
    """Subjects management."""
    subjects = Subject.objects.filter(user=request.user)
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            return redirect('subjects')
    else:
        form = SubjectForm()

    return render(request, 'subjects.html', {'subjects': subjects, 'form': form})


# ── API Views ──────────────────────────────────────────────

@login_required
@require_POST
def api_toggle_habit(request):
    """Toggle a habit's completion for today."""
    data = json.loads(request.body)
    habit_id = data.get('habit_id')
    habit = get_object_or_404(Habit, id=habit_id, user=request.user)
    today = date.today()

    log, created = HabitLog.objects.get_or_create(
        habit=habit, date=today,
        defaults={'completed': True}
    )
    if not created:
        log.completed = not log.completed
        log.save()

    # Update streak
    if log.completed:
        habit.streak_count += 1
        if habit.streak_count > habit.best_streak:
            habit.best_streak = habit.streak_count
    else:
        habit.streak_count = max(0, habit.streak_count - 1)
    habit.save()

    return JsonResponse({
        'completed': log.completed,
        'streak': habit.streak_count,
    })


@login_required
@require_POST
def api_log_session(request):
    """Log a completed focus timer session."""
    data = json.loads(request.body)
    subject_id = data.get('subject_id')
    duration = data.get('duration_minutes', 25)

    session = StudySession.objects.create(
        user=request.user,
        subject_id=subject_id,
        duration_minutes=duration,
        start_time=timezone.now() - timedelta(minutes=duration),
        end_time=timezone.now(),
    )

    # Update profile
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.total_study_minutes += duration
    profile.points += duration
    profile.save()

    return JsonResponse({'success': True, 'session_id': session.id})


@login_required
@require_POST
def api_log_mood(request):
    """Log mood for today."""
    data = json.loads(request.body)
    mood_score = data.get('mood_score')
    today = date.today()

    entry, created = MoodEntry.objects.update_or_create(
        user=request.user, date=today,
        defaults={'mood_score': mood_score}
    )
    return JsonResponse({'success': True, 'mood': entry.mood_score})


@login_required
@require_POST
def api_add_habit(request):
    """Add a new habit."""
    data = json.loads(request.body)
    name = data.get('name', '').strip()
    if not name:
        return JsonResponse({'error': 'Name is required'}, status=400)

    habit = Habit.objects.create(user=request.user, name=name)
    return JsonResponse({'id': habit.id, 'name': habit.name})


@login_required
@require_POST
def api_complete_goal(request):
    """Mark a goal as complete."""
    data = json.loads(request.body)
    goal_id = data.get('goal_id')
    goal = get_object_or_404(Goal, id=goal_id, user=request.user)
    goal.completed = True
    goal.save()

    # Award points
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.points += 50
    profile.save()

    return JsonResponse({'success': True})

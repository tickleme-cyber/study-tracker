from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import (
    Subject, StudySession, Goal, FlashcardDeck, Flashcard,
    Habit, HabitLog, MoodEntry, Achievement, UserProfile
)
from django.utils import timezone
from datetime import timedelta, date
import random


class Command(BaseCommand):
    help = 'Seed the database with demo data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create demo user
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={'email': 'demo@studytracker.com', 'is_staff': True}
        )
        if created:
            user.set_password('demo1234')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created demo user (demo / demo1234)'))

        # Create profile
        profile, _ = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'total_study_minutes': 4500,
                'current_streak': 15,
                'best_streak': 28,
                'points': 2840,
            }
        )

        # Create subjects
        subjects_data = [
            ('Mathematics', '#7c3aed', '📐'),
            ('Physics', '#3b82f6', '⚛️'),
            ('Chemistry', '#10b981', '⚗️'),
            ('Biology', '#f97316', '🧬'),
            ('English', '#ef4444', '📝'),
            ('Computer Science', '#06b6d4', '💻'),
        ]

        subjects = []
        for name, color, icon in subjects_data:
            subj, _ = Subject.objects.get_or_create(
                name=name, user=user,
                defaults={'color': color, 'icon': icon}
            )
            subjects.append(subj)

        # Create study sessions (last 30 days)
        if not StudySession.objects.filter(user=user).exists():
            for i in range(60):
                day_offset = random.randint(0, 30)
                session_date = timezone.now() - timedelta(days=day_offset)
                subj = random.choice(subjects)
                duration = random.choice([25, 25, 45, 45, 60])
                StudySession.objects.create(
                    user=user,
                    subject=subj,
                    start_time=session_date,
                    end_time=session_date + timedelta(minutes=duration),
                    duration_minutes=duration,
                    notes=f'Studied {subj.name} for {duration} minutes',
                )
            self.stdout.write(self.style.SUCCESS('Created 60 study sessions'))

        # Create goals
        goals_data = [
            ('Master Calculus', 'Complete all calculus chapters', 40, 28, 'high'),
            ('Physics Revision', 'Revise all physics concepts', 30, 15, 'medium'),
            ('Chemistry Lab Prep', 'Prepare for lab practical', 10, 8, 'high'),
            ('Read English Novel', 'Finish the assigned novel', 15, 5, 'low'),
        ]

        for title, desc, target, completed, priority in goals_data:
            Goal.objects.get_or_create(
                title=title, user=user,
                defaults={
                    'description': desc,
                    'subject': subjects[0] if 'Calc' in title else subjects[1],
                    'target_hours': target,
                    'completed_hours': completed,
                    'deadline': date.today() + timedelta(days=random.randint(7, 60)),
                    'priority': priority,
                }
            )

        # Create flashcard decks
        decks_data = [
            ('Biology Basics', subjects[3], [
                ('Mitochondria', 'The powerhouse of the cell. Produces ATP via cellular respiration.'),
                ('Photosynthesis', '6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂. Converts sunlight to glucose.'),
                ('DNA', 'Deoxyribonucleic acid. Double helix structure carrying genetic info.'),
                ('Cell Membrane', 'Selectively permeable phospholipid bilayer.'),
                ('Ribosome', 'Organelle for protein synthesis. Found on rough ER or free.'),
            ]),
            ('Physics Formulas', subjects[1], [
                ('Newton\'s 2nd Law', 'F = ma (Force = mass × acceleration)'),
                ('Kinetic Energy', 'KE = ½mv² (half mass times velocity squared)'),
                ('Ohm\'s Law', 'V = IR (Voltage = Current × Resistance)'),
                ('Wave Speed', 'v = fλ (speed = frequency × wavelength)'),
            ]),
        ]

        for deck_name, subj, cards in decks_data:
            deck, _ = FlashcardDeck.objects.get_or_create(
                name=deck_name, user=user,
                defaults={'subject': subj}
            )
            for front, back in cards:
                Flashcard.objects.get_or_create(
                    deck=deck, front=front,
                    defaults={'back': back, 'difficulty': random.choice(['easy', 'medium', 'hard'])}
                )

        # Create habits
        habits_data = [
            'Revise yesterday\'s notes',
            'Solve 10 practice MCQs',
            'No phone during study block',
            '30 min reading',
        ]

        for name in habits_data:
            habit, _ = Habit.objects.get_or_create(
                name=name, user=user,
                defaults={'streak_count': random.randint(3, 15), 'best_streak': random.randint(10, 30)}
            )
            # Create some logs
            for i in range(7):
                d = date.today() - timedelta(days=i)
                HabitLog.objects.get_or_create(
                    habit=habit, date=d,
                    defaults={'completed': random.random() > 0.3}
                )

        # Create achievements
        achievements_data = [
            ('🔥 First Streak', 'Complete a 7-day study streak', 'Study for 7 consecutive days', 25),
            ('📚 Bookworm', 'Study for 100 hours total', 'Accumulate 100 hours of study time', 100),
            ('🎯 Goal Crusher', 'Complete 5 study goals', 'Mark 5 goals as completed', 50),
            ('🃏 Card Master', 'Review 500 flashcards', 'Review flashcards 500 times', 75),
            ('⏱️ Focus Champion', 'Complete 50 focus sessions', 'Finish 50 Pomodoro sessions', 50),
        ]

        for name, desc, criteria, points in achievements_data:
            Achievement.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'criteria': criteria, 'icon': name[:2], 'points': points}
            )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
        self.stdout.write(self.style.SUCCESS('Login: demo / demo1234'))

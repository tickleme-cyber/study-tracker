from django import forms
from .models import Subject, Goal, FlashcardDeck, Flashcard, Habit, MoodEntry, Doubt


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'color', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Data Structures'}),
            'color': forms.TextInput(attrs={'class': 'form-input color-picker', 'type': 'color'}),
            'icon': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., 📚, 💻, 📐'}),
        }


class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['title', 'description', 'subject', 'target_hours', 'deadline', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Master Dynamic Programming'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Optional details...'}),
            'subject': forms.Select(attrs={'class': 'form-input'}),
            'target_hours': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.5', 'min': '0.5'}),
            'deadline': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'priority': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)
        self.fields['subject'].required = False


class FlashcardDeckForm(forms.ModelForm):
    class Meta:
        model = FlashcardDeck
        fields = ['name', 'subject']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Big-O Notation'}),
            'subject': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)


class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['front', 'back', 'difficulty']
        widgets = {
            'front': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Question or prompt...'}),
            'back': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Answer or explanation...'}),
            'difficulty': forms.Select(attrs={'class': 'form-input'}),
        }


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g., Solve 2 LeetCode problems'}),
            'description': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Optional details...'}),
        }


class MoodEntryForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['mood_score', 'notes']
        widgets = {
            'mood_score': forms.Select(attrs={'class': 'form-input'}),
            'notes': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'How did studying go today?'}),
        }


class DoubtForm(forms.ModelForm):
    class Meta:
        model = Doubt
        fields = ['subject', 'question', 'answer']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-input'}),
            'question': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'What are you stuck on?'}),
            'answer': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Resolution or answer (optional)...'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subject'].queryset = Subject.objects.filter(user=user)
        self.fields['subject'].required = False
        self.fields['answer'].required = False

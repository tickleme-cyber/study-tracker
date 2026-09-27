# 📚 Study Tracker

A comprehensive, minimalist study tracking web application built with **Django**, **HTML5**, **CSS3**, and **Vanilla JavaScript**.

---

## ✨ Features

- ⏱️ **Focus Timer & Study Sessions**: Built-in Pomodoro/Focus timer with real-time logging of study durations.
- 🎯 **Goals & Target Tracking**: Set target study hours, priority levels, and track progress with interactive visuals.
- 🗂️ **Flashcards & Spaced Repetition**: Create custom flashcard decks and practice with difficulty-based filtering.
- 🔥 **Habit Tracking & Streaks**: Daily habit check-ins and streak monitoring to build consistent study routines.
- 😊 **Mood & Productivity Tracker**: Log daily study moods and notes to understand learning habits.
- ❓ **Doubt Solver / Notes**: Save subject-specific doubts and questions to review or resolve later.
- 🏆 **Gamification & Achievements**: Earn badges, study points, and maintain streaks as you complete goals.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/tickleme-cyber/study-tracker.git
   cd study-tracker
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **(Optional) Seed sample data:**
   ```bash
   python manage.py seed_data
   ```

6. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

7. Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Database:** SQLite (Default / configurable)

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).

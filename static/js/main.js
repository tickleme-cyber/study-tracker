/* ═══════════════════════════════════════════════════════════
   MINIMALIST STUDY PLANNER — Main JavaScript
   ═══════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initStatCounters();
    initFlashcardDemo();
    initFocusTimerDemo();
    initStreakCalendar();
    initHabitDemo();
    initMoodDemo();
    initSeatingChart();
    initExamCountdown();
    initCareerExplorer();
    initBrainBattle();
    initDoubtLog();
});

/* ── Navbar ─────────────────────────────────────────────── */
function initNavbar() {
    const toggle = document.getElementById('nav-toggle');
    const links = document.getElementById('nav-links');
    if (!toggle || !links) return;

    toggle.addEventListener('click', () => {
        links.classList.toggle('open');
    });

    // Close menu on link click
    links.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', () => links.classList.remove('open'));
    });

    // Navbar scroll effect
    window.addEventListener('scroll', () => {
        const navbar = document.getElementById('navbar');
        if (window.scrollY > 50) {
            navbar.style.borderBottomColor = 'rgba(16, 185, 129, 0.25)';
        } else {
            navbar.style.borderBottomColor = 'rgba(255, 255, 255, 0.07)';
        }
    });
}

/* ── Animated Stat Counters ─────────────────────────────── */
function initStatCounters() {
    const counters = document.querySelectorAll('.stat-number[data-target]');
    if (!counters.length) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(c => observer.observe(c));
}

function animateCounter(el) {
    const target = parseFloat(el.dataset.target);
    const suffix = el.dataset.suffix || '';
    const isDecimal = el.dataset.decimal === 'true';
    const duration = 2000;
    const start = performance.now();

    function update(now) {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        // Ease out cubic
        const ease = 1 - Math.pow(1 - progress, 3);
        let current = ease * target;

        if (isDecimal) {
            el.textContent = current.toFixed(1) + '★';
        } else if (target >= 100) {
            el.textContent = Math.floor(current).toLocaleString() + '+' + suffix;
        } else {
            el.textContent = Math.floor(current) + suffix;
        }

        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }

    requestAnimationFrame(update);
}

/* ── Flashcard Demo ─────────────────────────────────────── */
function initFlashcardDemo() {
    const inner = document.getElementById('flashcard-inner');
    const demo = document.getElementById('flashcard-demo');
    if (!inner || !demo) return;

    const cards = [
        { front: 'Mitochondria', back: 'The powerhouse of the cell. Responsible for producing ATP through cellular respiration.' },
        { front: 'Photosynthesis', back: '6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂. Plants convert sunlight into glucose.' },
        { front: 'Pythagorean Theorem', back: 'a² + b² = c². Relates the sides of a right triangle.' },
        { front: 'Newton\'s 2nd Law', back: 'F = ma. Force equals mass times acceleration.' },
        { front: 'DNA Structure', back: 'Double helix made of nucleotides. Bases: A-T, G-C paired by hydrogen bonds.' },
    ];

    let currentIndex = 0;

    function updateCard() {
        document.getElementById('flashcard-front-text').textContent = cards[currentIndex].front;
        document.getElementById('flashcard-back-text').textContent = cards[currentIndex].back;
        document.getElementById('fc-counter').textContent = `${currentIndex + 1} / ${cards.length}`;
        inner.classList.remove('flipped');
    }

    demo.addEventListener('click', (e) => {
        if (e.target.closest('.btn-fc-nav')) return;
        inner.classList.toggle('flipped');
    });

    document.getElementById('fc-prev')?.addEventListener('click', () => {
        if (currentIndex > 0) { currentIndex--; updateCard(); }
    });

    document.getElementById('fc-next')?.addEventListener('click', () => {
        if (currentIndex < cards.length - 1) { currentIndex++; updateCard(); }
    });
}

/* ── Focus Timer Demo ───────────────────────────────────── */
function initFocusTimerDemo() {
    const display = document.getElementById('demo-timer-display');
    const btn = document.getElementById('demo-timer-btn');
    const ring = document.getElementById('timer-ring-progress');
    if (!display || !btn || !ring) return;

    const totalSeconds = 25 * 60; // 25 minutes
    let remaining = totalSeconds;
    let interval = null;
    let running = false;
    const circumference = 2 * Math.PI * 52; // r=52

    function updateDisplay() {
        const m = Math.floor(remaining / 60);
        const s = remaining % 60;
        display.textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
        const progress = (totalSeconds - remaining) / totalSeconds;
        ring.style.strokeDashoffset = circumference * (1 - progress);
    }

    btn.addEventListener('click', () => {
        if (running) {
            clearInterval(interval);
            running = false;
            btn.innerHTML = '<span>▶</span> Start Focus';
        } else {
            running = true;
            btn.innerHTML = '<span>⏸</span> Pause';
            interval = setInterval(() => {
                remaining--;
                updateDisplay();
                if (remaining <= 0) {
                    clearInterval(interval);
                    running = false;
                    remaining = totalSeconds;
                    btn.innerHTML = '<span>▶</span> Start Focus';
                    updateDisplay();
                }
            }, 1000);
        }
    });

    // Sound buttons
    document.querySelectorAll('.timer-sounds .sound-btn').forEach(b => {
        b.addEventListener('click', function() {
            this.closest('.timer-sounds').querySelectorAll('.sound-btn').forEach(s => s.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

/* ── Streak Calendar Demo ───────────────────────────────── */
function initStreakCalendar() {
    const cal = document.getElementById('streak-calendar');
    if (!cal) return;

    // Generate 28 days of streak data
    const days = 28;
    const streakPattern = [
        1,1,1,0,1,1,1,
        1,0,1,1,1,1,0,
        1,1,1,1,0,1,1,
        1,1,1,1,1,1,1
    ];

    for (let i = 0; i < days; i++) {
        const day = document.createElement('div');
        day.className = 'streak-day' + (streakPattern[i] ? ' active' : '');
        day.title = `Day ${i + 1}`;
        day.addEventListener('mouseenter', function() {
            if (this.classList.contains('active')) {
                this.style.boxShadow = '0 0 16px rgba(249, 115, 22, 0.6)';
            }
        });
        day.addEventListener('mouseleave', function() {
            if (this.classList.contains('active')) {
                this.style.boxShadow = '0 0 8px rgba(249, 115, 22, 0.4)';
            }
        });
        cal.appendChild(day);
    }
}

/* ── Habit Tracker Demo ─────────────────────────────────── */
function initHabitDemo() {
    const checks = document.querySelectorAll('#demo-habits .habit-check');
    const counter = document.getElementById('habit-counter');
    if (!checks.length || !counter) return;

    function updateCount() {
        const done = document.querySelectorAll('#demo-habits .habit-check:checked').length;
        counter.textContent = `👍 ${done}/${checks.length} done today`;
    }

    checks.forEach(cb => cb.addEventListener('change', updateCount));
}

/* ── Mood Tracker Demo ──────────────────────────────────── */
function initMoodDemo() {
    const emojis = document.getElementById('mood-emojis');
    const label = document.getElementById('mood-day-label');
    const week = document.getElementById('mood-week');
    if (!emojis || !label || !week) return;

    const moodMap = { 1: '😞', 2: '😐', 3: '😊' };
    let currentDay = 1;
    const moods = [];

    emojis.querySelectorAll('.mood-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const mood = parseInt(this.dataset.mood);
            moods.push(mood);

            // Add mood dot
            const dot = document.createElement('div');
            dot.className = 'mood-dot';
            dot.textContent = moodMap[mood];
            week.appendChild(dot);

            // Animate selection
            emojis.querySelectorAll('.mood-btn').forEach(b => b.classList.remove('selected'));
            this.classList.add('selected');

            setTimeout(() => {
                this.classList.remove('selected');
                currentDay++;
                if (currentDay <= 7) {
                    label.textContent = `Day ${currentDay} of 7 — how did it go?`;
                } else {
                    label.textContent = 'Week complete! Your mood trend is logged 📊';
                    emojis.style.opacity = '0.4';
                    emojis.style.pointerEvents = 'none';
                }
            }, 400);
        });
    });
}

/* ── Seating Chart Demo ─────────────────────────────────── */
function initSeatingChart() {
    const students = document.querySelectorAll('.student-tag');
    const seats = document.querySelectorAll('.seat');
    if (!students.length || !seats.length) return;

    let draggedStudent = null;

    students.forEach(tag => {
        tag.addEventListener('dragstart', function(e) {
            draggedStudent = this;
            this.classList.add('dragging');
            e.dataTransfer.effectAllowed = 'move';
        });

        tag.addEventListener('dragend', function() {
            this.classList.remove('dragging');
            draggedStudent = null;
        });
    });

    seats.forEach(seat => {
        seat.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('drag-over');
        });

        seat.addEventListener('dragleave', function() {
            this.classList.remove('drag-over');
        });

        seat.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-over');
            if (draggedStudent && !this.classList.contains('occupied')) {
                this.textContent = draggedStudent.dataset.student;
                this.classList.add('occupied');
                draggedStudent.style.display = 'none';
            }
        });
    });
}

/* ── Exam Countdown ─────────────────────────────────────── */
function initExamCountdown() {
    const dateInput = document.getElementById('exam-date');
    const chaptersInput = document.getElementById('exam-chapters');
    const result = document.getElementById('exam-result');
    if (!dateInput || !chaptersInput || !result) return;

    function calculate() {
        const examDate = dateInput.value;
        const chapters = parseInt(chaptersInput.value) || 0;
        if (!examDate || !chapters) {
            result.textContent = 'Pick your exam date and remaining chapter count above.';
            return;
        }

        const today = new Date();
        today.setHours(0, 0, 0, 0);
        const exam = new Date(examDate);
        const diffDays = Math.ceil((exam - today) / (1000 * 60 * 60 * 24));

        if (diffDays <= 0) {
            result.innerHTML = '<strong style="color: #ef4444;">Exam day is here or has passed!</strong> 🏃‍♂️';
            return;
        }

        const chapPerDay = (chapters / diffDays).toFixed(1);
        result.innerHTML = `
            <strong style="color: #7c3aed;">${diffDays} days</strong> remaining.
            Study <strong style="color: #f97316;">${chapPerDay} chapters/day</strong> to finish on time.
            That's about <strong>${Math.ceil(chapters / Math.ceil(diffDays / 7))} chapters/week</strong>. You got this! 💪
        `;
    }

    dateInput.addEventListener('change', calculate);
    chaptersInput.addEventListener('input', calculate);
}

/* ── Career Explorer ────────────────────────────────────── */
function initCareerExplorer() {
    const tags = document.querySelectorAll('.career-tag');
    const result = document.getElementById('career-result');
    if (!tags.length || !result) return;

    const careers = {
        science: ['🔬 Research Scientist', '🧬 Biotechnologist', '⚗️ Pharmaceutical Researcher', '🏥 Medical Doctor', '🌍 Environmental Scientist'],
        commerce: ['📊 Chartered Accountant', '💹 Financial Analyst', '🏦 Investment Banker', '📈 Business Consultant', '🛒 Supply Chain Manager'],
        arts: ['🎨 UX Designer', '📝 Content Strategist', '🎬 Film Director', '📚 Journalist', '🏛️ Historian'],
        tech: ['💻 Software Engineer', '🤖 AI/ML Engineer', '☁️ Cloud Architect', '🔒 Cybersecurity Analyst', '📱 Mobile Developer'],
    };

    tags.forEach(tag => {
        tag.addEventListener('click', function() {
            tags.forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            const stream = this.dataset.stream;
            const list = careers[stream];

            result.innerHTML = `<ul class="career-list">${list.map(c => `<li>${c}</li>`).join('')}</ul>`;
        });
    });
}

/* ── BrainBattle Demo ───────────────────────────────────── */
function initBrainBattle() {
    const startBtn = document.getElementById('btn-start-battle');
    const battleArea = document.getElementById('battle-area');
    if (!startBtn || !battleArea) return;

    const questions = [
        {
            q: 'What is the chemical formula for water?',
            options: ['H₂O', 'CO₂', 'NaCl', 'O₂'],
            answer: 0
        },
        {
            q: 'Who wrote "Romeo and Juliet"?',
            options: ['Charles Dickens', 'William Shakespeare', 'Jane Austen', 'Mark Twain'],
            answer: 1
        },
        {
            q: 'What is the square root of 144?',
            options: ['10', '11', '12', '14'],
            answer: 2
        },
    ];

    startBtn.addEventListener('click', function() {
        this.style.display = 'none';
        battleArea.style.display = 'block';

        const q = questions[Math.floor(Math.random() * questions.length)];
        document.getElementById('battle-question').textContent = q.q;

        const optionsContainer = document.getElementById('battle-options');
        optionsContainer.innerHTML = '';
        const resultDiv = document.getElementById('battle-result');
        resultDiv.textContent = '';

        q.options.forEach((opt, i) => {
            const btn = document.createElement('button');
            btn.className = 'battle-option';
            btn.textContent = opt;
            btn.addEventListener('click', () => {
                optionsContainer.querySelectorAll('.battle-option').forEach(b => {
                    b.style.pointerEvents = 'none';
                });

                if (i === q.answer) {
                    btn.classList.add('correct');
                    resultDiv.innerHTML = '<span style="color: #10b981;">🎉 Correct! +50 points</span>';
                } else {
                    btn.classList.add('wrong');
                    optionsContainer.children[q.answer].classList.add('correct');
                    resultDiv.innerHTML = '<span style="color: #ef4444;">❌ Wrong! The correct answer is highlighted.</span>';
                }

                // Reset after delay
                setTimeout(() => {
                    startBtn.style.display = '';
                    startBtn.innerHTML = '<span>⚔️</span> Play Again';
                    battleArea.style.display = 'none';
                }, 3000);
            });
            optionsContainer.appendChild(btn);
        });
    });
}

/* ── Doubt Log Demo ─────────────────────────────────────── */
function initDoubtLog() {
    const items = document.querySelectorAll('.doubt-item');
    const answer = document.getElementById('doubt-answer');
    if (!items.length || !answer) return;

    const answers = {
        balance: `<strong>Balancing: Fe + O₂ → Fe₂O₃</strong><br><br>
            Step 1: Count atoms — Fe: 1→2, O: 2→3<br>
            Step 2: Balance Fe — put 4 in front of Fe<br>
            Step 3: Balance O — put 3 in front of O₂<br>
            Step 4: Check Fe₂O₃ — put 2 in front<br><br>
            <strong style="color: #10b981;">4Fe + 3O₂ → 2Fe₂O₃ ✓</strong>`,
        derivative: `<strong>Finding d/dx (x³ + 2x)</strong><br><br>
            Apply the power rule: d/dx(xⁿ) = nxⁿ⁻¹<br><br>
            • d/dx(x³) = 3x²<br>
            • d/dx(2x) = 2<br><br>
            <strong style="color: #10b981;">Answer: 3x² + 2 ✓</strong>`,
        seasons: `<strong>Why do seasons change?</strong><br><br>
            Earth's axis is tilted at 23.5° relative to its orbital plane around the Sun.<br><br>
            • When your hemisphere tilts <em>toward</em> the Sun → Summer (more direct sunlight)<br>
            • When it tilts <em>away</em> → Winter (less direct sunlight)<br>
            • Spring & Autumn occur during transition periods<br><br>
            <strong style="color: #10b981;">It's the tilt, not the distance from the Sun! ✓</strong>`,
    };

    items.forEach(item => {
        item.addEventListener('click', function() {
            items.forEach(i => i.style.borderColor = 'rgba(255,255,255,0.06)');
            this.style.borderColor = 'rgba(124, 58, 237, 0.4)';

            const doubt = this.dataset.doubt;
            answer.innerHTML = '';

            // Typewriter effect
            const html = answers[doubt];
            answer.innerHTML = '<span class="typing-cursor">▋</span>';

            // Simple reveal: show content directly with a fade
            setTimeout(() => {
                answer.innerHTML = html;
                answer.style.animation = 'fadeInUp 0.4s ease-out';
            }, 300);
        });
    });
}

/* ── Chat Demo (Simple) ────────────────────────────────── */
const chatInput = document.getElementById('chat-input');
const chatSend = document.getElementById('chat-send');
const chatContainer = document.getElementById('chat-container');

if (chatInput && chatSend && chatContainer) {
    let questionsUsed = 0;
    const maxQuestions = 3;

    const sampleAnswers = {
        default: "That's a great question! To get full AI-powered answers, sign up for a free account. Here's a brief overview based on your query...",
    };

    chatSend.addEventListener('click', () => {
        const question = chatInput.value.trim();
        if (!question || questionsUsed >= maxQuestions) return;

        questionsUsed++;
        chatContainer.innerHTML = `
            <div style="margin-bottom: 8px;">
                <strong style="color: #7c3aed;">You:</strong> ${question}
            </div>
            <div>
                <strong style="color: #3b82f6;">AI:</strong> ${sampleAnswers.default}
            </div>
        `;
        chatInput.value = '';

        const footnote = document.querySelector('.demo-footnote');
        if (footnote) {
            footnote.textContent = `${questionsUsed}/${maxQuestions} demo questions used · sign up free for unlimited, personalized answers`;
        }
    });

    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') chatSend.click();
    });
}

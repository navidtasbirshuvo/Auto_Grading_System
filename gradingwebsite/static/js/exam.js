
let examState = {
    currentQuestion: 0,
    totalQuestions: 25,
    timeRemaining: 0,
    answers: {},
    isSubmitted: false,
    isPaused: false
};


function initializeExam() {
    loadExamData();
    startTimer();
    loadQuestion(0);
    generateQuestionNavigation();
    setupEventListeners();
}

function loadExamData() {
    examState.totalQuestions = 25;
    examState.timeRemaining = 90 * 60;
}

function startTimer() {
    const timerInterval = setInterval(() => {
        if (examState.isPaused || examState.isSubmitted) {
            clearInterval(timerInterval);
            return;
        }

        examState.timeRemaining--;
        updateTimerDisplay();

        if (examState.timeRemaining <= 0) {
            clearInterval(timerInterval);
            autoSubmitExam();
        }
    }, 1000);
}

function updateTimerDisplay() {
    const minutes = Math.floor(examState.timeRemaining / 60);
    const seconds = examState.timeRemaining % 60;
    const timerElement = document.getElementById('exam-timer');

    if (timerElement) {
        timerElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;

        if (examState.timeRemaining <= 300) { 
            timerElement.classList.add('timer-warning');
        }
    }
}

function loadQuestion(questionIndex) {
    examState.currentQuestion = questionIndex;

    
    const currentQuestionElement = document.getElementById('current-question');
    if (currentQuestionElement) {
        currentQuestionElement.textContent = questionIndex + 1;
    }

    
    updateProgressBar();

  
    updateNavigationButtons();


    updateQuestionNavigation();

  
    loadQuestionContent(questionIndex);
}

function loadQuestionContent(questionIndex) {
    const questions = [
        {
            id: 1,
            type: 'multiple-choice',
            question: 'What is the time complexity of the quicksort algorithm in the average case?',
            options: ['O(n)', 'O(n log n)', 'O(n²)', 'O(2^n)'],
            correctAnswer: 'b'
        },
    ];

    const question = questions[questionIndex] || questions[0];
    updateQuestionDisplay(question);
}

function updateQuestionDisplay(question) {
    console.log('Loading question:', question);
}

function generateQuestionNavigation() {
    const navContainer = document.querySelector('.question-nav .d-flex');
    if (!navContainer) return;

    navContainer.innerHTML = '';

    for (let i = 1; i <= examState.totalQuestions; i++) {
        const questionBtn = document.createElement('div');
        questionBtn.className = `question-number ${i === 1 ? 'current' : 'unanswered'}`;
        questionBtn.textContent = i;
        questionBtn.onclick = () => goToQuestion(i - 1);
        navContainer.appendChild(questionBtn);
    }
}

function updateQuestionNavigation() {
    const navButtons = document.querySelectorAll('.question-number');
    navButtons.forEach((btn, index) => {
        btn.className = 'question-number';

        if (index === examState.currentQuestion) {
            btn.classList.add('current');
        } else if (examState.answers[index]) {
            btn.classList.add('answered');
        } else {
            btn.classList.add('unanswered');
        }
    });
}

function updateProgressBar() {
    const progress = ((examState.currentQuestion + 1) / examState.totalQuestions) * 100;
    const progressBar = document.querySelector('.progress-bar');

    if (progressBar) {
        progressBar.style.width = progress + '%';
        progressBar.setAttribute('aria-valuenow', progress);
    }

    const progressText = document.querySelector('.progress + div .small:last-child');
    if (progressText) {
        progressText.textContent = Math.round(progress) + '% Complete';
    }
}

function updateNavigationButtons() {
    const prevBtn = document.querySelector('button[onclick="previousQuestion()"]');
    const nextBtn = document.querySelector('button[onclick="nextQuestion()"]');

    if (prevBtn) {
        prevBtn.disabled = examState.currentQuestion === 0;
    }

    if (nextBtn) {
        if (examState.currentQuestion === examState.totalQuestions - 1) {
            nextBtn.innerHTML = '<span class="material-icons me-2">send</span>Submit';
            nextBtn.onclick = () => submitExam();
        } else {
            nextBtn.innerHTML = 'Next<span class="material-icons ms-2">arrow_forward</span>';
            nextBtn.onclick = () => nextQuestion();
        }
    }
}

function nextQuestion() {
    if (examState.currentQuestion < examState.totalQuestions - 1) {
        saveCurrentAnswer();
        loadQuestion(examState.currentQuestion + 1);
    }
}

function previousQuestion() {
    if (examState.currentQuestion > 0) {
        saveCurrentAnswer();
        loadQuestion(examState.currentQuestion - 1);
    }
}

function goToQuestion(questionIndex) {
    if (questionIndex >= 0 && questionIndex < examState.totalQuestions) {
        saveCurrentAnswer();
        loadQuestion(questionIndex);
    }
}

function saveCurrentAnswer() {
   
    const selectedAnswer = document.querySelector(`input[name="question${examState.currentQuestion + 1}"]:checked`);

    if (selectedAnswer) {
        examState.answers[examState.currentQuestion] = selectedAnswer.value;
    }

   
    localStorage.setItem('examState', JSON.stringify(examState));
}

function markForReview() {
  
    const questionBtn = document.querySelector(`.question-number:nth-child(${examState.currentQuestion + 1})`);
    if (questionBtn) {
        questionBtn.classList.add('flagged');
        questionBtn.style.border = '2px solid #F59E0B';
    }

    alert('Question marked for review');
}

function pauseExam() {
    if (confirm('Are you sure you want to pause this exam? Your progress will be saved.')) {
        examState.isPaused = true;
        saveCurrentAnswer();

        
        localStorage.setItem('examState', JSON.stringify(examState));
        window.location.href = 'current-exams.html';
    }
}

function submitExam() {
    saveCurrentAnswer();

    const answeredCount = Object.keys(examState.answers).length;
    const unansweredCount = examState.totalQuestions - answeredCount;

    let message = `You have answered ${answeredCount} out of ${examState.totalQuestions} questions.`;
    if (unansweredCount > 0) {
        message += `\n${unansweredCount} questions remain unanswered.`;
    }
    message += '\n\nAre you sure you want to submit your exam?';

    if (confirm(message)) {
        examState.isSubmitted = true;

        submitToServer();

        localStorage.removeItem('examState');

        alert('Exam submitted successfully!');
        window.location.href = 'student-results.html';
    }
}

function autoSubmitExam() {
    alert('Time is up! Your exam will be submitted automatically.');
    examState.isSubmitted = true;
    submitToServer();
    localStorage.removeItem('examState');
    window.location.href = 'student-results.html';
}

function submitToServer() {
    console.log('Submitting exam:', examState);

    const examData = {
        examId: 'exam_123',
        studentId: 'student_456',
        answers: examState.answers,
        timeSpent: (90 * 60) - examState.timeRemaining,
        submittedAt: new Date().toISOString()
    };

    console.log('Exam data submitted:', examData);
}

function setupEventListeners() {
    
    window.addEventListener('beforeunload', function(e) {
        if (!examState.isSubmitted) {
            e.preventDefault();
            e.returnValue = 'Are you sure you want to leave? Your exam progress may be lost.';
        }
    });

    setInterval(() => {
        if (!examState.isSubmitted && !examState.isPaused) {
            saveCurrentAnswer();
        }
    }, 30000); 
}


document.addEventListener('DOMContentLoaded', function() {
    
    const savedState = localStorage.getItem('examState');
    if (savedState) {
        examState = JSON.parse(savedState);
    }

    initializeExam();
});

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Choice, UserAnswer
from .forms import QuizForm

@login_required
def take_quiz(request, quiz_id):
    """
    View for taking a quiz.
    - Fetches quiz and its questions.
    - Processes form submission and evaluates the score.
    """
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        form = QuizForm(request.POST, quiz=quiz)
        if form.is_valid():
            correct_answers = 0
            total_questions = quiz.questions.count()

            for question in quiz.questions.all():
                selected_choice_id = form.cleaned_data.get(f'question_{question.id}')
                selected_choice = Choice.objects.get(id=selected_choice_id)

                # Store user answer
                UserAnswer.objects.create(
                    user=request.user,
                    question=question,
                    selected_choice=selected_choice
                )

                if selected_choice.is_correct:
                    correct_answers += 1

            score = (correct_answers / total_questions) * 100
            return render(request, 'quiz_result.html', {'quiz': quiz, 'score': score})

    else:
        form = QuizForm(quiz=quiz)

    return render(request, 'take_quiz.html', {'quiz': quiz, 'form': form})

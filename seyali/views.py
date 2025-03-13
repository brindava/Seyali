from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import ContentForm, CustomUserCreationForm, QuizForm
from .models import Content, Quiz

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('content_list')
    else:
        return redirect('login')

@login_required
def content_list(request):
    contents = Content.objects.all()
    return render(request, 'content_list.html', {'contents': contents})

@login_required
def content_upload(request):
    if not request.user.is_teacher:
        return HttpResponseForbidden("You are not authorized to upload content.")
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES)
        if form.is_valid():
            content = form.save(commit=False)
            content.uploaded_by = request.user
            content.save()
            return redirect('content_list')
    else:
        form = ContentForm()
    return render(request, 'content_upload.html', {'form': form})

@login_required
def content_delete(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    if not request.user.is_teacher:
        return HttpResponseForbidden("You are not authorized to delete content.")
    if request.user == content.uploaded_by or request.user.is_superuser or request.user.is_teacher:
        content.delete()
    return redirect('content_list')

@login_required
def content_edit(request, content_id):
    content = get_object_or_404(Content, id=content_id)
    if not request.user.is_teacher:
        return HttpResponseForbidden("You are not authorized to edit content.")
    if request.method == 'POST':
        form = ContentForm(request.POST, request.FILES, instance=content)
        if form.is_valid():
            form.save()
            return redirect('content_list')
    else:
        form = ContentForm(instance=content)
    return render(request, 'content_edit.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('content_list')  # Redirect to content list after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Quiz Views
"""@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz_detail.html', {'quiz': quiz})

@login_required
def quiz_create(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quiz_list')
    else:
        form = QuizForm()
    return render(request, 'quiz_form.html', {'form': form})

@login_required
def quiz_edit(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz_list')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'quiz_form.html', {'form': form})

@login_required
def quiz_delete(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == 'POST':
        quiz.delete()
        return redirect('quiz_list')
    return render(request, 'quiz_confirm_delete.html', {'quiz': quiz})"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Content, Quiz, Question, Choice, UserAnswer
from .forms import ContentForm, CustomUserCreationForm, QuizForm

@login_required
def content_list(request):
    contents = Content.objects.all()
    return render(request, 'content_list.html', {'contents': contents})

@login_required
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz_list.html', {'quizzes': quizzes})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        form = QuizForm(request.POST, quiz=quiz)
        if form.is_valid():
            correct_answers = 0
            total_questions = quiz.questions.count()

            for question in quiz.questions.all():
                selected_choice_id = form.cleaned_data.get(f'question_{question.id}')
                selected_choice = Choice.objects.get(id=selected_choice_id)

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
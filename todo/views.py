from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Todo

def indexPage(request):
    todos = Todo.objects.filter(user_id=request.user.id)
    return render(request, 'index.html', {'todos': todos})

@login_required
def create_todo(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Todo.objects.create(title=title, user_id=request.user.id)
            messages.success(request, 'Todo created successfully!')
        else:
            messages.error(request, 'Title cannot be empty.')
        return redirect('index')
    return render(request, 'create_todo.html')

@login_required
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user_id=request.user.id)
    if request.method == 'POST':
        todo.delete()
        messages.success(request, 'Todo deleted successfully!')
        return redirect('index')

@login_required
def toggle_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user_id=request.user.id)
    if request.method == 'POST':
        todo.isDone = not todo.isDone
        todo.save()
        messages.success(request, 'Todo status updated successfully!')
        return redirect('index')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            messages.success(request, 'Signup successful!')
            return redirect('index')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


@login_required
def search_todo(request):
    query = request.GET.get('q')
    if query:
        search = Todo.objects.filter(user_id=request.user.id, title__icontains=query)
    else:
        search = Todo.objects.filter(user_id=request.user.id)
    return render(request, 'search.html', {'search': search})
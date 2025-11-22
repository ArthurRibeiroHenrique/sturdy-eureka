from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Task

# Registrar um usuário

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("task_list")
    else:
        form = UserCreationForm()
        
    return render(request, "register.html", {"form": form})

# Login

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("task_list")
    
    else:
        form = AuthenticationForm()
    
    return render(request, "login.html", {"form": form})

# Logout

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request,  "task_list.html", {"tasks": tasks})

@login_required
def task_create(request):
    if request.method == "POST":
        Task.objects.create(
            user=request.user,
            title=request.POST["title"]
        )
        return render(request, "task_create.html")

@login_required
def task_toggle(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    task.done = not task.done
    task.save()
    return redirect("task_list")       
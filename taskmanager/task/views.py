from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1!=password2:
            messages.error(request, 'Passwords do not match')
            # return render(request, 'register.html')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            # return render(request, 'register.html')
        else:
            user=User.objects.create_user(username=username,password=password1)
            messages.success(request,"registeration Successful , Please login !")
            return redirect('login')
    return render(request,'task/register.html')   


def login_view(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        
        user=authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request,'task/login.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def index(request):
    tasks = Task.objects.all().order_by('-created_at')
    return render(request,'task/index.html',{'tasks': tasks})

# def task(request):
#     return render(request,'task/task_form.html')

from .models import Task
from .forms import TaskForm

def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('task_list')
            return redirect('index')  # go back to task list
    else:
        form = TaskForm()
    return render(request, 'task/task_form.html', {'form': form})


def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('index')  # Change to your list view name index upd
    else:
        form = TaskForm(instance=task)
    return render(request, 'task/task_form.html', {'form': form})


def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':  # Confirm delete before actually deleting
        task.delete()
        return redirect('index')  # change to your actual list view name index upd
    return render(request, 'task/task_confirm_delete.html', {'task': task})          
        
def home(request):
    tasks = Task.objects.all().order_by('-created_at')  # newest first
    return render(request, 'home.html', {'tasks': tasks})
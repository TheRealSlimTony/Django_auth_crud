from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
import requests as ri

import asyncio
import httpx

async def fetch_facts(api_key, limit):
    headers = {'X-Api-Key': api_key}
    url = f'https://api.api-ninjas.com/v1/facts?limit={limit}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=10.0)
    if response.status_code == httpx.codes.ok:
        fact = response.json()[0]['fact']
    else:
        fact = 'Error fetching fact'
    return fact

async def home(request):
    api_key = 'v6thHnV+uQHj1bIVxSvv3w==km3pAo6anq2N1iPi'
    limit = 1
    fact = await fetch_facts(api_key, limit)
    print(request.method)

    if fact == "Error fetching fact":
        fact = "Por favor saquenme de latam"

    return render(request, 'home.html', {'fact': fact})
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'usuario ya existe'
                })
        else:
            return render(request, 'signup.html', {
                'error': 'contrase;a no coinciden',
                'form': UserCreationForm
            })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        print('Get')
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        if request.method == 'POST':

            user = request.POST['username']
            password = request.POST['password']
            # print(user, password)
            user = authenticate(request, username=user, password=password)

            if user is None:
                return render(request, 'signin.html', {
                    'form': AuthenticationForm,
                    'error': 'Contrase;a o usuario no validos'
                })
            else:
                login(request, user)
                return redirect('home')

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            if request.method == 'POST':
                print(request.POST)
                form = TaskForm(request.POST)
                new_task = form.save(commit=False)
                new_task.user = request.user
                new_task.save()
            return redirect('tasks')

        except:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'no valid data '
            })

@login_required
def task_detail(request, task_id):

    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)

        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': "error actualizando la tarea"
            })

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

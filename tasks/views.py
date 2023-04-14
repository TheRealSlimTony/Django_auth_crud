import asyncio
import json
import os

import httpx
# Create your views here.
import requests
import requests as ri
from asgiref.sync import sync_to_async
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TaskForm
from .models import Snippet, Task


async def get_ip(access_key):
    
    # Make a request to a third-party service to retrieve your public IP address
    ip_response = requests.get('https://api.ipify.org')
    ip_address = ip_response.text

    # Construct the API URL with the IP address and access key
    url = f'http://api.ipstack.com/{ip_address}?access_key={access_key}'

    # Make the API request and store the response in a variable
    response = requests.get(url)

    # Check the status code of the response to ensure it was successful
    if response.status_code == 200:
        # If the request was successful, parse the response data as JSON
        location_data = response.json()
        latitud = location_data.get('latitude')
        longitud = location_data.get('longitude')
        ip = location_data.get('ip')
        print(latitud,longitud,ip)

        return latitud,longitud,ip
    else:
        # If the request was unsuccessful, raise an exception or handle the error
        response.raise_for_status()

async def fetch_facts(api_key, limit):
    headers = {'X-Api-Key': api_key}
    url = f'https://api.api-ninjas.com/v1/facts?limit={limit}'
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=100.0)
    if response.status_code == httpx.codes.ok:
        fact = response.json()[0]['fact']
    else:
        fact = 'Error fetching fact'
    return fact

async def home(request):
    facts_key = os.environ.get('facts_key')
    ip_key = os.environ.get('ip_key')
    x = 'AIzaSyBWMJCBePTwSIG2Q_e3nORCm68IegukHTY'
    limit = 1
    fact = ""
    fact = await fetch_facts(facts_key, limit)
    latitud,longitud,ip = await get_ip(ip_key)
    print(request.method)
    print(ip)

    if fact == "Error fetching fact" or fact == "":
        fact = "Por favor saquenme de latam"
    
    # wrap the render function with sync_to_async
    render_func = sync_to_async(render)
    rendered = await render_func(request, 'home.html', {'fact': fact,'ip_info':ip,'latitud':latitud,'longitud':longitud,'x':x})
    return rendered

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
                print(user)
                print(type(user))
                return redirect('home')

def snippets(request):
   
    snippets = Snippet.objects.all()
    print(snippets)
    
    return render(request, 'snippets.html', {
        'tasks': snippets
    })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    snippets = Snippet.objects.all()
    print(tasks,snippets)
    
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(
        user = request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        'tasks': tasks
    })

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

@login_required
def snippet(request):
    if request.method == 'GET':
        print('es un get')
        return render(request,'snippet.html')
    
    else:
        if request.method == 'POST':
            title = request.POST['title']
            tag = request.POST['tag']
            snippet = request.POST['snippet']
            print(title,tag,snippet,request.user)
            snippet = Snippet(title=title,language=tag, descripcion = snippet,user=request.user)
            snippet.save()
            return render(request,'snippet.html')



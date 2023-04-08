from django.shortcuts import render, redirect
from .models import Room, Message

from django.http import HttpResponse,JsonResponse

# Create your views here.


def home(request):
    # print(request.POST)
    # if request.method == 'POST':

        # room_name = request.POST['room_name']
        # username = request.POST['username']
        # print(room_name, username)
        # Room.objects.create(room_name)
    #     return render(request, 'home_chat.html')

    # else:
    #     if request.method == 'GET':
    #         return render(request, 'home_chat.html')
    return render(request,'home_chat.html')


def room(request,room_name):

    username = request.GET.get('username')
    
    room_details = Room.objects.get(name=room_name)
    print('++++++++++++++++',username,room_details)
    if request.method == 'POST':
        return render(request, 'room.html',{
            'room':room_name,
            'username':username,
            'room_details':room_details
        })
    else:
        if request.method == 'GET':
            return render(request, 'room.html',{
            'room':room_name,
            'username':username,
            'room_details':room_details
        })

def check_view(request):

    room_name = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room_name).exists():
        return redirect('/chat/home/room/'+room_name+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room_name)
        new_room.save()
        return redirect('/chat/home/room/'+room_name+'/?username='+username)


def send(request):
    message = request.POST['message']
    room = request.POST['room_id']
    username = request.POST['username']
    # print('******************************',request.POST)

    message = Message.objects.create(user=username,room=room,value=message)
    message.save()
    return HttpResponse('Message send')

def get_messages(request,room):
    room_details =  Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    print(messages)
    return JsonResponse({"messages":list(messages.values())})

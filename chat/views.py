import os
from django.shortcuts import render, redirect
from .models import Room, Message

from django.http import HttpResponse,JsonResponse
import qrcode
import datetime

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

def create_qr2(request):
    # print(request.POST)
    
    # if request.method == 'POST':
    #     if 'Send' in request.POST:
    #         print(request.POST['QR_Request'])
    #         qr_code_name_requested = request.POST['QR_Request']
    #         path_name = qr_creation(qr_code_name_requested)

    #         return render(request,'create_qr.html',{
    #             'qr_code_name_requested':qr_code_name_requested,
    #             'path_name':path_name
    #         })
        # elif 'Delete' in request.POST:
        #     for file in os.listdir("static\img\QRs"):
        #         os.remove(os.path.join("static\img\QRs", file))
        #         print(file)


    return render(request,'create_qr.html')


def qr_creation(qr_code_requested):
    # create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    # add data to the QR code
    qr.add_data(qr_code_requested)

    # compile the QR code
    qr.make(fit=True)

    # create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # save the image
    current_time = datetime.datetime.now()
    time_string = current_time.strftime('%Y%m%d_%H%M%S')
    path = os.path.join("static", "img", "QRs", "QR_code_{}.png".format(time_string)).replace("\\","/")
    img.save(path)
    return path

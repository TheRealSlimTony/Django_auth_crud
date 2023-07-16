import base64

import qrcode
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from PIL import Image
import cv2
import numpy as np


from .models import Message, Room

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
    return render(request, "home_chat.html")


def room(request, room_name):
    username = request.GET.get("username")

    room_details = Room.objects.get(name=room_name)
    print("++++++++++++++++", username, room_details)
    if request.method == "POST":
        return render(
            request,
            "room.html",
            {"room": room_name, "username": username, "room_details": room_details},
        )
    else:
        if request.method == "GET":
            return render(
                request,
                "room.html",
                {"room": room_name, "username": username, "room_details": room_details},
            )


def check_view(request):
    room_name = request.POST["room_name"]
    username = request.POST["username"]

    if Room.objects.filter(name=room_name).exists():
        return redirect("/chat/home/room/" + room_name + "/?username=" + username)
    else:
        new_room = Room.objects.create(name=room_name)
        new_room.save()
        return redirect("/chat/home/room/" + room_name + "/?username=" + username)


def send(request):
    message = request.POST["message"]
    room = request.POST["room_id"]
    username = request.POST["username"]
    # print('******************************',request.POST)

    message = Message.objects.create(user=username, room=room, value=message)
    message.save()
    return HttpResponse("Message send")


def get_messages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    print(messages)
    return JsonResponse({"messages": list(messages.values())})


def create_qr(request):
    if request.method == "POST":
        if "Send" in request.POST:
            print(request.POST["QR_Request"])
            qr_code_name_requested = request.POST["QR_Request"]
            response = qr_creation(qr_code_name_requested)
            image_data = base64.b64encode(response.content).decode("utf-8")

            return render(
                request,
                "create_qr.html",
                {
                    "qr_code_name_requested": qr_code_name_requested,
                    "qr_image": image_data,
                },
            )

    return render(request, "create_qr.html")


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

    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")

    return response


def read_qr(request):
    if request.method == "POST":
        qr_file = request.FILES["qr-code"]
        img = cv2.imdecode(np.fromstring(qr_file.read(), np.uint8), cv2.IMREAD_COLOR)
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)
        print(data)

        return render(request, "read_qr.html", {"qr_decoded": data})

    return render(request, "read_qr.html")

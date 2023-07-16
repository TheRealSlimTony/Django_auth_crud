import os
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
import openai
import pytesseract
from PIL import Image


def home(request):
    openai.api_key = os.environ.get("chatgpt")

    if request.method == "GET":
        print("esto es un get")

    else:
        print(request.POST)
        request_to_do = request.POST["request_to_do"]
        text = request.POST["text"]
        print(request_to_do, text)

        analized_info = analize_info(request_to_do, text)

    return render(request, "home_chatgpt.html", {"analized_info": analized_info})


def read_img(request):
    openai.api_key = os.environ.get("chatgpt")

    if request.method == "POST":
        qr_file = request.FILES["qr-code"]
        image = Image.open(qr_file)
        text = pytesseract.image_to_string(image)
        # analized_info = analize_info("sumarized the following text", text)
        # print(text, analized_info)

        return render(
            request,
            "upload_img_text.html",
            {"txt_img": text, "analized_info": "analized_info"},
        )

    return render(request, "upload_img_text.html")


def analize_info(prompt, text=None):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": "give all response in json format :{} {} ".format(
                    prompt, text
                ),
            }
        ],
    )
    return completion.choices[0].message.content

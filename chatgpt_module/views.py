import base64
import os
from openai import OpenAI
import pytesseract
from cryptography.fernet import Fernet
from django.shortcuts import get_object_or_404, render
from PIL import Image
import requests


def home(request):
    OPENAI_API_KEY = os.environ.get("chatgpt")

    if request.method == "GET":
        return render(request, "home_chatgpt.html", {"analized_info": ""})

    else:
        print(request.POST)
        context = request.POST["context"]
        instruction = request.POST["instruction"]
        input_v = request.POST["input"]
        output_v = request.POST["output"]
        request_to_do = context + instruction + input_v + output_v

        print(request_to_do)

        analized_info = analize_info(request_to_do, "")

        return render(request, "home_chatgpt.html", {"analized_info": analized_info})


def chat_pdf(request):
    return render(request, "chat_pdf.html")


def read_img(request):
    OPENAI_API_KEY = os.environ.get("chatgpt")

    if request.method == "POST":
        qr_file = request.FILES["qr-code"]
        image = Image.open(qr_file)
        text = pytesseract.image_to_string(image)
        print(text)
        analized_info = analize_info("sumarized the following text", text)
        print(text, analized_info)

        return render(
            request,
            "upload_img_text.html",
            {"txt_img": text, "analized_info": analized_info},
        )

    return render(request, "upload_img_text.html")


def analize_info(prompt, text):
    api_key = os.environ.get("chatgpt")
    # gets API Key from environment variable OPENAI_API_KEY
    client = OpenAI()

    # Non-streaming:
    print("----- standard request -----")
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return completion.choices[0].message.content
    # Streaming:
    # print("----- streaming request -----")
    # stream = client.chat.completions.create(
    #     model="gpt-4",
    #     messages=[
    #         {
    #             "role": "user",
    #             "content": prompt,
    #         },
    #     ],
    #     stream=True,
    # )
    # for chunk in stream:
    #     if not chunk.choices:
    #         continue
    #     print(chunk.choices[0].delta.content, end="")
    # print()


def encrypt_text_view(request):
    if request.method == "POST":
        # print(request.POST)
        text = request.POST["text_to_encrypt"]
        print(text)
        encryption_key = generate_key()
        encrypted_text = encrypt_text(encryption_key, text)
        return render(
            request,
            "encrypt_text.html",
            {"encrypted_text": encrypted_text, "encryption_key": encryption_key},
        )

    return render(request, "encrypt_text.html")


def generate_key():
    return Fernet.generate_key()


def encrypt_text(key, text):
    fernet = Fernet(key)
    encrypted_text = fernet.encrypt(text.encode())
    return encrypted_text


def decrypt_text_view(request):
    if request.method == "POST":
        text = request.POST["text_to_decrypt"]
        key_string = request.POST["key"]

        try:
            # Convert the key from string to bytes
            key_bytes = base64.urlsafe_b64decode(key_string.encode())

            # Create a Fernet instance using the key
            fernet = Fernet(key_bytes)

            # Decrypt the text
            decrypted_text = fernet.decrypt(text.encode()).decode()

            return render(
                request, "decrypt_text.html", {"decrypted_text": decrypted_text}
            )
        except Exception as e:
            print("Error:", e)
            return render(request, "decrypt_text.html", {"decrypted_text": "Error"})

    return render(request, "decrypt_text.html")

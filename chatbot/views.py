from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
import csv
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from dotenv import find_dotenv, load_dotenv
from langchain import LLMChain, OpenAI, PromptTemplate
import os
import openai
from pydantic import BaseModel
import requests


# Create your views here.
def home(request):
    # URL del endpoint FastAPI
    url = "http://127.0.0.1:8001/search_question/"

    # Datos JSON "quemados" para enviar
    data = {"prompt": "tell me some of the inventions of c"}

    # Realizar la solicitud POST con JSON
    response = requests.post(url, json=data)
    print(response)

    # Verificar que la solicitud fue exitosa
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse(
            {"error": "No se pudo obtener datos desde FastAPI"},
            status=response.status_code,
        )

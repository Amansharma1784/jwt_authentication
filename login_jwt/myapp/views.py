from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from .serializers import UserSerializer

class StudentsAPI(viewsets.ModelViewSet):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=Student.objects.all()
    serializer_class=UserSerializer
    





# def login_page(request):

#     return render(request,'login.html')

# views.py
from django.shortcuts import render, redirect
import requests
from django.contrib import messages


def get_data(acess_token):
    access_token = acess_token
    protected_url = "http://127.0.0.1:8000/studentapi/"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(protected_url, headers=headers)
    return  response.json()

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        token_url = "http://127.0.0.1:8000/gettoken/"
        response = requests.post(token_url, data={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            tokens = response.json()
            # print(tokens["access"])
            data = get_data(tokens['access'])
            print(data)
            # messages.success(request, 'Login successful.')


            # return HttpResponse()
            
            # return render(request, 'login.html', {'access': tokens['access'], 'refresh': tokens['refresh']})
        
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'login.html')

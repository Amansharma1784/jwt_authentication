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
import json


# def get_data(acess_token):
#     access_token = acess_token
#     protected_url = "http://127.0.0.1:8000/studentapi/"
#     headers = {"Authorization": f"Bearer {access_token}"}
#     response = requests.get(protected_url, headers=headers)
#     json_data=json.dumps(response.json(),indent=4)
#     return  render(requests,'show_data.html',{'json_data':json_data})

def add_data(request):
    if request.method == 'GET':
        access_token=request.GET.get('access_token')

        return render(request, 'add_data.html')
    
    elif request.method=='POST':
        name=request.POST.get('name')
        roll=request.POST.get('roll')
        city=request.POST.get('city')
        # access_token = request.POST.get('access_token')
        
        access_token = request.session.get('access_token')
        print("@@@@@@@@@",request.session.items())
        if not access_token:
            return HttpResponse("Access token missing", status=400)

        headers = {"Authorization": f"Bearer {access_token}"}

        data={'name':name,
              'roll':roll,
              'city':city}
        protected_url="http://127.0.0.1:8000/studentapi/"
        response=requests.post(protected_url,headers=headers,data=data)

        if response.status_code in [200, 201]:
            messages.success(request, 'Student added successfully!')
        else:
            messages.error(request, f"Failed to add student: {response.text}")

    return redirect('login')

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
            access_token=tokens['access']
            # print(access_token)
            # data=access_token
            # add_data(request,data)
            protected_url="http://127.0.0.1:8000/studentapi/"
            headers={"Authorization": f"Bearer {access_token}"}
            response1 = requests.get(protected_url, headers=headers)

            if response1.status_code==200:
                # data=json.dumps(response1.json(),indent=4)
                # return HttpResponse(data)
                token = request.session['access_token'] = access_token
                return render(request,'show_data.html',{'data':response1.json()})
            # else:
            # print("Failed to fetch protected data:", response1.status_code)
            # print(tokens["access"])
            # data = get_data(tokens['access'])
            # print(data)
            # messages.success(request, 'Login successful.')
            # return HttpResponse()
            
            # return render(request, 'login.html', {'access': tokens['access'], 'refresh': tokens['refresh']})
        
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'login.html')


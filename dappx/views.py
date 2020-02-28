# dappx/views.py

from django.shortcuts import render
from dappx.forms import UserForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from dappx.models import Post
from dappx.forms import PostForm
import openpyxl
import csv

def index(request):
    if request.method == 'GET':
        return render(request,'dappx/index.html')
    else:
        MyPostForm = PostForm(request.POST, request.FILES)

        if MyPostForm.is_valid():
            post = Post()
            post. = MyPostForm.cleaned_data["uploadfile"]
            post.save()
            saved = True

        upload_file = request.FILES["excel_file"]
        data = list()
        if upload_file.name.endswith('.xlsx'):
            wb = openpyxl.load_workbook(upload_file)
            worksheet = wb["Sheet1"]
            print(worksheet)

            for row in worksheet.iter_rows():
                row_data = list()
                for cell in row:
                    row_data.append(str(cell.value))
                data.append(row_data)

        elif upload_file.name.endswith('.csv'):
            file_data = upload_file.read().decode("utf-8")
            lines = file_data.split("\n")
            for line in lines:
                row_data = list()
                fields = line.split(",")
                for cell in fields:
                    row_data.append(str(cell))
                data.append(row_data)


        return render(request,'dappx/index.html', {"excel_data":data})



@login_required
def special(request):
    return HttpResponse("You are logged in !")
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'dappx/registration.html',
                          {'user_form':user_form,
                           'registered':registered})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponseRedirect(reverse('user_login'))
    else:
        return render(request, 'dappx/login.html', {})


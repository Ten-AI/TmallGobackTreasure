from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import json

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from tmall import models


def index(request):
    # context = {}
    # context['hello'] = 'Hello World!'
    return render(request, 'index.html')


@csrf_exempt
def login(request):
    global message
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print(password)
        try:
            user = models.TLoginUser.objects.get(user_id=username)
            if user.password == password:
                redirect()
            else:
                message = "用户名或密码不正确！"
        except:
            message = "用户名或密码不正确！"
        return JsonResponse(dict({"message": message}))

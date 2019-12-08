from random import randrange

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import json

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from pyecharts.charts import Bar
from pyecharts import options as opts
from rest_framework.views import APIView

from tmall import models


def index(request):
    # context = {}
    # context['hello'] = 'Hello World!'
    return render(request, 'index.html')


@csrf_exempt
def login(request):
    message = ''
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print(password)
        try:
            user = models.TLoginUser.objects.get(user_id=username)
            if user.password == password:
                request.session['user_id'] = user
                request.session['is_login'] = True
                message = "yes"
            else:
                message = "用户名或密码不正确！"
        except:
            message = "用户名或密码不正确！"
        return JsonResponse(dict({"message": message}))


def base(request):
    return render(request, 'plain.html')


def bartest(request):
    c = (
        Bar()
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
            .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
            .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))

    )
    return JsonResponse(c.dump_options_with_quotes())





def response_as_json(data):
    json_str = json.dumps(data)
    response = HttpResponse(
        json_str,
        content_type="application/json",
    )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def json_response(data, code=200):
    data = {
        "code": code,
        "msg": "success",
        "data": data,
    }
    return response_as_json(data)


def json_error(error_string="error", code=500, **kwargs):
    data = {
        "code": code,
        "msg": error_string,
        "data": {}
    }
    data.update(kwargs)
    return response_as_json(data)


JsonResponse = json_response
JsonError = json_error


def action_type_bar() -> Bar:
    models.TMerchant.objects.objects

    c = (
        Bar()
            .add_xaxis(["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"])
            .add_yaxis("商家A", [randrange(0, 100) for _ in range(6)])
            .add_yaxis("商家B", [randrange(0, 100) for _ in range(6)])
            .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
            .dump_options_with_quotes()
    )
    return c


class ChartView(APIView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(json.loads(action_type_bar()))


class IndexView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'plain.html')

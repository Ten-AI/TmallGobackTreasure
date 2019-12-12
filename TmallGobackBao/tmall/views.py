from random import randrange

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import json

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from pyecharts.charts import Bar, Line, Pie, EffectScatter
from pyecharts import options as opts
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
from rest_framework.views import APIView
from django.db import connection
from tmall import models


cursor = connection.cursor()
session =None

def index(request):
    # context = {}
    # context['hello'] = 'Hello World!'
    return render(request, 'index.html')


@csrf_exempt
def login(request):
    message = ''
    request.session.flush()
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        print(password)
        try:
            user = models.TMerchant.objects.get(merchant_id=username)
            print(user.merchant_id, "密码", user.password)
            if user.password == password:
                request.session['user_id'] = user.merchant_id
                request.session['is_login'] = True
                message = "yes1"
            else:
                print("用户名或密码不正确！")
                message = "用户名或密码不正确！"
        except Exception as ex:
            print("出现如下异常%s" %ex)
            message = "出错！"
        return JsonResponse(dict({"message": message}))


@csrf_exempt
def login_as_yunying(request):
    message = ''
    request.session.flush()
    if request.method == "POST":
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        try:
            user = models.TLoginUser.objects.get(user_id=username)
            print(user.user_id, "密码", user.password)
            if user.password == password:
                request.session['user_id'] = user.user_id
                request.session['is_login'] = True
                message = "yes2"
            else:
                print("用户名或密码不正确！")
                message = "用户名或密码不正确！"
        except Exception as ex:
            print("出现如下异常%s" %ex)
            message = "出错！"
        return JsonResponse(dict({"message": message}))


def base(request):
    return render(request, 'plain.html')


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


def action_type_bar(session, charts_type):
    if not session['is_login']:
        return None
    user_id = session['user_id']
    if charts_type == 'gmv':
        cursor.execute("SELECT * FROM t_commodity_sale_info WHERE merchant_id = "+user_id+"  ORDER BY CAST(month_ AS UNSIGNED INTEGER)")

        res = cursor.fetchall()
        xs = list(map(lambda x: x[2], res))
        ys = list(map(lambda x: int(x[1]), res))
        bar = (
            Bar({"theme": ThemeType.MACARONS})
                .add_xaxis(xs).add_yaxis("gmv变化情况", ys)
                .set_series_opts(itemstyle_opts={
                "normal": {
                    "color": Faker.rand_color(),
                    "barBorderRadius": [10, 10, 10, 10],
                    "shadowColor": '#32ca12',
                }}).set_global_opts(
                title_opts=opts.TitleOpts(title="gmv变化情况"),
                datazoom_opts=[opts.DataZoomOpts(),
                               opts.DataZoomOpts(type_="inside")]).dump_options_with_quotes()
        )
        line = (
            Line().add_xaxis(xs).add_yaxis("gmv变化曲线", ys, is_smooth=True,
                                           areastyle_opts=opts.AreaStyleOpts(opacity=0.5,
                                                                             color=Faker.rand_color()))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="gmv变化曲线"),
                xaxis_opts=opts.AxisOpts(
                    axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                    is_scale=False,
                    boundary_gap=False,
                ),
                ).dump_options_with_quotes()
        )
        return [json.loads(bar), json.loads(line)]
    elif charts_type == 'gender':
        cursor.execute("SELECT gender,`count` FROM t_gender_distribute WHERE merchant_id = "+user_id)
        res = cursor.fetchall()
        def to_text(l):
            if l[0] == '0.0':
                return ["女性", l[1]]
            elif l[0] == '1.0':
                return ["男性", l[1]]
            else:
                return ["未知", l[1]]
        res = map(to_text, res)
        print(res)
        pie = (
            Pie().add("用户性别分布", list(res),
                      radius=["25%", "75%"],
                      center=["50%", "50%"],
                      rosetype="radius",
                      )
                .set_global_opts(title_opts=opts.TitleOpts(title="用户性别分布"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        ).dump_options_with_quotes()
        return [json.loads(pie)]
    elif charts_type == 'area':
        cursor.execute("SELECT area_name,`count` FROM t_area_distribute WHERE merchant_id = "+user_id)
        res = cursor.fetchall()
        xs = list(map(lambda x: x[0], res))
        ys = list(map(lambda x: int(x[1]), res))
        bar = (
            Bar({"theme": ThemeType.MACARONS})
                .add_xaxis(xs).add_yaxis("用户地域分布情况", ys)
                .set_series_opts(itemstyle_opts={
                "normal": {
                    "color": Faker.rand_color(),
                    "barBorderRadius": [10, 10, 10, 10],
                    "shadowColor": '#32ca12',
                }}).set_global_opts(
                title_opts=opts.TitleOpts(title="用户地域分布情况"),
                datazoom_opts=[opts.DataZoomOpts(),
                               opts.DataZoomOpts(type_="inside")]).dump_options_with_quotes()
        )
        pie = (
            Pie().add("用户性别分布", list(res),
                      radius=["25%", "75%"],
                      center=["50%", "50%"],
                      rosetype="radius",
                      )
                # .set_global_opts(title_opts=opts.TitleOpts(title="用户地域分布"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        ).dump_options_with_quotes()
        return [json.loads(bar), json.loads(pie)]
    elif charts_type == 'age':
        cursor.execute("SELECT age_range,`count` FROM t_age_distribute WHERE merchant_id = "+user_id)
        res = cursor.fetchall()
        label = ["未知", "[18-]", "[18,24]", "[25,29]", "[30,34]", "[35,39]", "[40,49]", "[50，60]", "[60+]"]
        xs = list(map(lambda x: label[int(float(x[0]))], res))
        ys = list(map(lambda x: int(x[1]), res))
        bar = (
            Bar({"theme": ThemeType.MACARONS})
                .add_xaxis(xs).add_yaxis("用户年龄分布", ys)
                .set_series_opts(itemstyle_opts={
                "normal": {
                    "color": Faker.rand_color(),
                    "barBorderRadius": [10, 10, 10, 10],
                    "shadowColor": '#32ca12',
                }}).set_global_opts(
                title_opts=opts.TitleOpts(title="用户年龄分布"),
                datazoom_opts=[opts.DataZoomOpts(),
                               opts.DataZoomOpts(type_="inside")]).dump_options_with_quotes()
        )
        line = (
            Line().add_xaxis(xs).add_yaxis("用户年龄分布", ys, is_smooth=True,
                                           areastyle_opts=opts.AreaStyleOpts(opacity=0.5,
                                                                             color=Faker.rand_color()))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="用户年龄分布"),
                xaxis_opts=opts.AxisOpts(
                    axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                    is_scale=False,
                    boundary_gap=False,
                ),
            ).dump_options_with_quotes()
        )
        return [json.loads(bar), json.loads(line)]
    elif charts_type == 'add_cart':
        cursor.execute("SELECT commodity_brand,`count` FROM add_to_cart_distribute_info WHERE merchant_id = "+user_id)
        res = cursor.fetchall()
        xs = list(map(lambda x: x[0], res))
        ys = list(map(lambda x: int(x[1]), res))
        bar = (
            Bar({"theme": ThemeType.MACARONS})
                .add_xaxis(xs).add_yaxis("用户添加购物车类别分布", ys)
                .set_series_opts(itemstyle_opts={
                "normal": {
                    "color": Faker.rand_color(),
                    "barBorderRadius": [10, 10, 10, 10],
                    "shadowColor": '#32ca12',
                }}).set_global_opts(
                title_opts=opts.TitleOpts(title="用户添加购物车类别分布"),
                datazoom_opts=[opts.DataZoomOpts(),
                               opts.DataZoomOpts(type_="inside")]).dump_options_with_quotes()
        )
        pie = (
            Pie().add("用户性别分布", list(res),
                      radius=["25%", "75%"],
                      center=["50%", "50%"],
                      rosetype="radius",
                      )
                # .set_global_opts(title_opts=opts.TitleOpts(title="用户地域分布"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            ).dump_options_with_quotes()
        return [json.loads(bar), json.loads(pie)]
    elif charts_type == 'add_favorite':
        cursor.execute("SELECT commodity_brand,`count` FROM add_to_favorite_distribute_info WHERE merchant_id = "+user_id)
        res = cursor.fetchall()
        xs = list(map(lambda x: x[0], res))
        ys = list(map(lambda x: int(x[1]), res))
        bar = (
            Bar({"theme": ThemeType.MACARONS})
                .add_xaxis(xs).add_yaxis("用户添加购物车类别分布", ys)
                .set_series_opts(itemstyle_opts={
                "normal": {
                    "color": Faker.rand_color(),
                    "barBorderRadius": [10, 10, 10, 10],
                    "shadowColor": '#32ca12',
                }}).set_global_opts(
                title_opts=opts.TitleOpts(title="用户添加购物车类别分布"),
                datazoom_opts=[opts.DataZoomOpts(),
                               opts.DataZoomOpts(type_="inside")]).dump_options_with_quotes()
        )
        pie = (
            Pie().add("用户性别分布", list(res),
                      radius=["25%", "75%"],
                      center=["50%", "50%"],
                      rosetype="radius",
                      )
                # .set_global_opts(title_opts=opts.TitleOpts(title="用户地域分布"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        ).dump_options_with_quotes()
        return [json.loads(bar), json.loads(pie)]
    elif charts_type == 'purchase':
        cursor.execute("SELECT commodity_brand,`count` FROM purchase_distribute_info WHERE merchant_id = "+user_id)
        res = cursor.fetchall()
        xs = list(map(lambda x: x[0], res))
        ys = list(map(lambda x: int(x[1]), res))
        bar = (
            Bar({"theme": ThemeType.MACARONS})
                .add_xaxis(xs).add_yaxis("用户添加购物车类别分布", ys)
                .set_series_opts(itemstyle_opts={
                "normal": {
                    "color": Faker.rand_color(),
                    "barBorderRadius": [10, 10, 10, 10],
                    "shadowColor": '#32ca12',
                }}).set_global_opts(
                title_opts=opts.TitleOpts(title="用户添加购物车类别分布"),
                datazoom_opts=[opts.DataZoomOpts(),
                               opts.DataZoomOpts(type_="inside")]).dump_options_with_quotes()
        )
        pie = (
            Pie().add("用户性别分布", list(res),
                      radius=["25%", "75%"],
                      center=["50%", "50%"],
                      rosetype="radius",
                      )
                # .set_global_opts(title_opts=opts.TitleOpts(title="用户地域分布"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        ).dump_options_with_quotes()
        return [json.loads(bar), json.loads(pie)]
    elif charts_type == 'click':
        cursor.execute("SELECT commodity_brand,`count` FROM click_distribute_info WHERE merchant_id = "+user_id)
        res = cursor.fetchall()
        xs = list(map(lambda x: x[0], res))
        ys = list(map(lambda x: int(x[1]), res))
        bar = (
            Bar({"theme": ThemeType.MACARONS})
                .add_xaxis(xs).add_yaxis("用户添加购物车类别分布", ys)
                .set_series_opts(itemstyle_opts={
                "normal": {
                    "color": Faker.rand_color(),
                    "barBorderRadius": [10, 10, 10, 10],
                    "shadowColor": '#32ca12',
                }}).set_global_opts(
                title_opts=opts.TitleOpts(title="用户添加购物车类别分布"),
                datazoom_opts=[opts.DataZoomOpts(),
                               opts.DataZoomOpts(type_="inside")]).dump_options_with_quotes()
        )
        pie = (
            Pie().add("用户性别分布", list(res),
                      radius=["25%", "75%"],
                      center=["50%", "50%"],
                      rosetype="radius",
                      )
                # .set_global_opts(title_opts=opts.TitleOpts(title="用户地域分布"))
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        ).dump_options_with_quotes()
        return [json.loads(bar), json.loads(pie)]


def action_type_bar2(session,charts_type):
    if not session['is_login']:
        return None
    if charts_type == 'price_month':
        cursor.execute("SELECT month_,`sum(price)` FROM yunying_all_price ORDER BY CAST(month_ AS UNSIGNED INTEGER)")
        res = cursor.fetchall()
        xs = list(map(lambda x: x[0], res))
        ys = list(map(lambda x: int(x[1]), res))
        bar = (
            Bar({"theme": ThemeType.MACARONS})
                .add_xaxis(xs).add_yaxis("平台整体交易额增长情况", ys)
                .set_series_opts(itemstyle_opts={
                "normal": {
                    "color": Faker.rand_color(),
                    "barBorderRadius": [10, 10, 10, 10],
                    "shadowColor": '#32ca12',
                }}).set_global_opts(
                toolbox_opts=opts.ToolboxOpts(),
                title_opts=opts.TitleOpts(title="平台整体交易额增长情况"),

                yaxis_opts=opts.AxisOpts(name="交易总额"),
                xaxis_opts=opts.AxisOpts(name="月份"),
                datazoom_opts=[opts.DataZoomOpts(),
                               opts.DataZoomOpts(type_="inside")]).dump_options_with_quotes()
        )
        line = (
            Line().add_xaxis(xs).add_yaxis("平台整体交易额增长情况", ys, is_smooth=True,
                                           areastyle_opts=opts.AreaStyleOpts(opacity=0.5,
                                                                             color=Faker.rand_color()))
                .set_global_opts(
                title_opts=opts.TitleOpts(title="平台整体交易额增长情况"),
                yaxis_opts=opts.AxisOpts(name="交易总额"),
                xaxis_opts=opts.AxisOpts(
                    name="月份",
                    axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                    is_scale=False,
                    boundary_gap=False,
                ),
            ).dump_options_with_quotes()
        )
        return [json.loads(bar), json.loads(line)]
    elif charts_type == 'brand':
        cursor.execute("SELECT brand_id,`count(*)` FROM yunying_brand")
        res = cursor.fetchall()
        xs = list(map(lambda x: x[0], res))
        ys = list(map(lambda x: int(x[1]), res))
        bar = (
            Bar({"theme": ThemeType.MACARONS})
                .add_xaxis(xs).add_yaxis("用户购买品牌分布情况", ys)
                .set_series_opts(itemstyle_opts={
                "normal": {
                    "color": Faker.rand_color(),
                    "barBorderRadius": [10, 10, 10, 10],
                    "shadowColor": '#32ca12',
                }}).set_global_opts(
                toolbox_opts=opts.ToolboxOpts(),
                title_opts=opts.TitleOpts(title="用户购买品牌分布情况"),

                yaxis_opts=opts.AxisOpts(name="交易商品数量"),
                xaxis_opts=opts.AxisOpts(name="品牌"),
                datazoom_opts=[opts.DataZoomOpts(),
                               opts.DataZoomOpts(type_="inside")]).dump_options_with_quotes()
        )
        pie = (
            Pie().add("用户购买品牌分布情况", list(res),
                      radius=["25%", "75%"],
                      center=["50%", "50%"],
                      rosetype="radius",
                      )
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        ).dump_options_with_quotes()

        return [json.loads(bar), json.loads(pie)]
    elif charts_type == 'category':
        cursor.execute("SELECT commodity_brand,`count(*)` FROM yunying_commodity")
        res = cursor.fetchall()
        xs = list(map(lambda x: x[0], res))
        ys = list(map(lambda x: int(x[1]), res))
        bar = (
            Bar({"theme": ThemeType.MACARONS})
                .add_xaxis(xs).add_yaxis("用户购买商品分类情况", ys)
                .set_series_opts(itemstyle_opts={
                "normal": {
                    "color": Faker.rand_color(),
                    "barBorderRadius": [10, 10, 10, 10],
                    "shadowColor": '#32ca12',
                }}).set_global_opts(
                toolbox_opts=opts.ToolboxOpts(),
                title_opts=opts.TitleOpts(title="用户购买商品分类情况"),

                # yaxis_opts=opts.AxisOpts(name="交易总额"),
                # xaxis_opts=opts.AxisOpts(name="月份"),
                datazoom_opts=[opts.DataZoomOpts(),
                               opts.DataZoomOpts(type_="inside")]).dump_options_with_quotes()
        )
        pie = (
            Pie().add("用户购买品牌分布情况", list(res),
                      radius=["25%", "75%"],
                      center=["50%", "50%"],
                      rosetype="radius",
                      )
                .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
        ).dump_options_with_quotes()

        return [json.loads(bar), json.loads(pie)]
    elif charts_type == 'laoguke':
        cursor.execute("SELECT '[0,10]' AS qujian,COUNT(merchant_id) FROM laoguke WHERE 10 > `sum(all_price)/count(merchant_id)` AND `sum(all_price)/count(merchant_id)` >= 0 UNION ALL "
                       "SELECT '[10,100]' AS qujian,COUNT(merchant_id) FROM laoguke WHERE 100 > `sum(all_price)/count(merchant_id)`AND `sum(all_price)/count(merchant_id)`  >= 10 UNION ALL "
                       "SELECT '[100,500]' AS qujian,COUNT(merchant_id) FROM laoguke WHERE 500 > `sum(all_price)/count(merchant_id)`AND `sum(all_price)/count(merchant_id)`  >= 100 UNION ALL "
                       "SELECT '[500,1000]' AS qujian,COUNT(merchant_id) FROM laoguke WHERE 1000 > `sum(all_price)/count(merchant_id)`AND `sum(all_price)/count(merchant_id)`  >= 500 UNION ALL "
                       "SELECT '[1000,2000]' AS qujian,COUNT(merchant_id) FROM laoguke WHERE 2000 > `sum(all_price)/count(merchant_id)`AND `sum(all_price)/count(merchant_id)`  >= 1000 UNION ALL "
                       "SELECT '[2000,5000]' AS qujian,COUNT(merchant_id) FROM laoguke WHERE 5000 > `sum(all_price)/count(merchant_id)`AND `sum(all_price)/count(merchant_id)`  >= 2000 UNION ALL "
                       "SELECT '[5000,10000]' AS qujian,COUNT(merchant_id) FROM laoguke WHERE 10000 > `sum(all_price)/count(merchant_id)`AND `sum(all_price)/count(merchant_id)`  >= 5000 UNION ALL "
                       "SELECT '[10000+]' AS qujian,COUNT(*) FROM laoguke WHERE `sum(all_price)/count(merchant_id)` >= 10000")
        res = cursor.fetchall()
        xs = list(map(lambda x: x[0], res))
        ys = list(map(lambda x: x[1], res))
        c = (
            EffectScatter()
                .add_xaxis(xs)
                .add_yaxis("", ys)
                .set_global_opts(
                title_opts=opts.TitleOpts(title="商家历史gmv分布图"),
                xaxis_opts=opts.AxisOpts(name="gmv区间", splitline_opts=opts.SplitLineOpts(is_show=True)),
                yaxis_opts=opts.AxisOpts(name="商家数量", splitline_opts=opts.SplitLineOpts(is_show=True)),
            )
        ).dump_options_with_quotes()
        line = (
            Line().add_xaxis(xs).add_yaxis("商家历史gmv分布图", ys, is_smooth=True,
                                           areastyle_opts=opts.AreaStyleOpts(opacity=0.5,
                                                                             color=Faker.rand_color()))
                .set_global_opts(
                title_opts=opts.TitleOpts(title=""),
                yaxis_opts=opts.AxisOpts(name="商家数量"),
                xaxis_opts=opts.AxisOpts(
                    name="gmv区间",
                    axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                    is_scale=False,
                    boundary_gap=False,
                ),
            ).dump_options_with_quotes()
        )
        return [json.loads(c), json.loads(line)]


def action_type_bar3(session, min, max):
    print(min)
    print(max)
    min = float(int(min))/100
    max = float(int(max))/100
    if not session['is_login']:
        return None
    user_id = session['user_id']
    sql = "select discount,ROI from t_roi where discount >={} and discount < {} and merchant_id = {}".format(min, max, user_id)
    cursor.execute(sql)
    res = cursor.fetchall()
    xs = list(map(lambda x: str(x[0]), res))
    ys = list(map(lambda x: (x[1]), res))
    print("xs:{}".format(xs))
    print(type(ys[0]))
    print("ys:{}".format(ys))
    line = (
        Line().add_xaxis(xs).add_yaxis("roi曲线", ys, is_smooth=True,
                                       areastyle_opts=opts.AreaStyleOpts(opacity=0.5,
                                                                         color=Faker.rand_color()))
            .set_global_opts(
            title_opts=opts.TitleOpts(title=""),
            yaxis_opts=opts.AxisOpts(name="roi曲线图"),
            xaxis_opts=opts.AxisOpts(
                name="折扣",
                axistick_opts=opts.AxisTickOpts(is_align_with_label=True),
                is_scale=False,
                boundary_gap=False,
            ),

        ).dump_options_with_quotes()
    )

    return [json.loads(line)]


class ChartView(APIView):
    def get(self, request, charts_type):
        return JsonResponse(action_type_bar(request.session, charts_type))


class ChartView2(APIView):
    def get(self, request, charts_type):
        return JsonResponse(action_type_bar2(request.session, charts_type))


class ChartView3(APIView):
    def get(self, request, min, max):
        return JsonResponse(action_type_bar3(request.session, min, max))


class IndexView(APIView):
    def get(self, request):
        return render(request, 'plain.html')


class IndexView2(APIView):
    def get(self, request):
        return render(request, 'plain2.html')

def start():
    print("stsart===")

start()


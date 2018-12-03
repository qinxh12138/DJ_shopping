import datetime
import json
import random

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render

from django_ajax.decorators import ajax

# Create your views here.
from apps.main.models import ShopCar, Shop, ShopImage, Order


@login_required
# def list(request):
#     car_list = ShopCar.objects.filter(user_id=request.user.id)
#     for car in car_list:
#         car.shop.imgs = car.shop.shopimage_set.filter(shop_id=car.shop.shop_id).first()
#
#     return render(request, 'carts.html', {'car_list': car_list})
def list(reqeust):
    car_list = ShopCar.objects.filter(user_id=reqeust.user.id)
    for car in car_list:
        car.shop.img = car.shop.shopimage_set \
            .filter(shop_id=car.shop_id) \
            .values_list('shop_img_id',flat=True) \
            .first()
    return render(reqeust, 'carts.html', {'car_list': car_list})

@ajax
@login_required
def add_car(request):
    result = {'status': 200, 'msg': 'ok'}
    if request.method == 'POST':
        try:
            number = request.POST.get("number")
            shop_id = request.POST.get('shop_id')
            if number and shop_id:
                car = ShopCar.objects.filter(shop_id=shop_id, user_id=request.user.id, status=1)
                update_number = 0
                if car.exists():
                    car.update(number=F('number') + number)
                else:
                    update_number = 1
                    car = ShopCar(number=number, shop_id=shop_id, user_id=request.user.id)
                    car.save()
                result.update(data=update_number)
                return JsonResponse(result)
        except Exception as e:
            result = {'status': 400, 'msg': '添加失败'}
            return JsonResponse(result)
    else:
        result = {'status': 2, 'msg': '不支持的请求方式'}
        return JsonResponse(result)


def update(request):
    pass


def detlete(request):
    pass




# 开始事务
@ajax
@login_required
def confirm(request):
    if request.method == 'POST':
        cars_str = request.POST.get('car')
        if cars_str:
            cars = json.loads(cars_str)
            try:
                # 开启事务
                with transaction.atomic():
                    # 生成订单
                    oid = product_order(request, cars)
                    #      做事务相关的操作
                    for car in cars:
                        ShopCar.objects.filter(car_id=car.get('car_id')).update(number=car.get('num'), order_id=oid)
                #    生成订单的操作
                return {'oid': oid}
            except Exception as e:
                transaction.rollback()
        else:
            pass


# 生成订单信息
def product_order(request, cars):
    # 第一步生成订单号  全站必须唯一   尽量大于8位
    user_id = request.user.id
    order_code = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}{random.randint(100000,999999)}"
    order = Order(order_code=order_code, user_id=user_id)
    order.save()
    return order.oid


@login_required
def order(request):
    oid = request.GET.get('oid')
    shops = ShopCar.objects.filter(order_id=oid)
    return render(request, 'confirm.html', {'shops': shops})
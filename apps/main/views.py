from django.shortcuts import render
from apps.main.models import Navigation, Category, Banner, PropertyValue


# Create your views here.
# def index(request):
#     nav_list = Navigation.objects.all()
#     cate_list = Category.objects.all()
#     banner_list = Banner.objects.all()
#     for cate in cate_list:
#         #  查询分类信息下的所有的商品信息
#         shops = cate.shop_set.all()
#         for shop in shops:
#             # 查询商品的图片信息
#             shop.img = shop.shopimage_set.values_list('shop_img_id', flat=True).first()
#         cate.shops = shops
#     return render(request, 'index.html', locals())




def index(request):
    nav_list = Navigation.objects.all()
    pro_list = PropertyValue.objects.all()
    banner_list = Banner.objects.all()
    cate_list = Category.objects.all()
    for cate in cate_list:
        shops = cate.shop_set.all()
        for shop in shops:
            shop.img = shop.shopimage_set.values_list('shop_img_id', flat=True).first()
        cate.shops = shops
    return render(request, 'index.html', locals())
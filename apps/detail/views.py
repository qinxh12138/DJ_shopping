from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from apps.main.models import Shop, ShopImage, PropertyValue, Review


def detail(request):
    sid = request.GET.get('sid')
    if sid:
        try:
            shops = Shop.objects.filter(shop_id=sid).values(
                'shop_id',
                'promote_price',
                'original_price',
                'stock', 'sub_title',
                'name'
            )
            if shops.exists():
                shop=shops.first()
                imgs=ShopImage.objects.filter(shop_id=shop.get('shop_id')).values('shop_img_id', 'type')
                shop.update(imgs=imgs)
                values = PropertyValue.objects.filter(shop_id=sid)
                reviews = Review.objects.filter(shop_id=sid)
                return render(request, 'detail.html', {'shop': shop, 'values': values, 'reviews': reviews})
            else:
                pass
        except Exception as e:
            print(e)
    else:
        return HttpResponse('404')


from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from apps.main.models import Shop


def search(request):
    q=request.GET.get('q')
    if q:
        shops = Shop.objects.filter(Q(name__icontains=q)|Q(sub_title__icontains=q))
        if shops:
            for shop in shops:
                shop.img = shop.shopimage_set.values_list('shop_img_id', flat=True).first()
            return render(request, 'search_detail.html',{'shops':shops})
        else:
            return HttpResponse(404)
    else:
        return HttpResponse(404)

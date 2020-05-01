from django.shortcuts import render
from django.http import HttpResponse, Http404

from .models import Product

import json
import re


# Create your views here.
def index(request):
    return render(request, 'openfoodfacts/index.html', {'header': True})


def get_products(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(name__icontains=q).order_by('-nutriscore', '-popularity')[:5]
        results = []
        for pr in products:
            product_json = {}
            product_json['label'] = pr.name + ' [' + pr.nutriscore + '] '
            product_json['id'] = pr.id
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = json.dumps('fail')
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def results(request):
    if request.method == "GET":
        # search for substitutes
        input = request.GET['search_input']
        # remove [] part
        input = re.sub(r'\[.*$', '', input).strip()
        # search substitute
        search_product = (Product.objects.filter(name__icontains=input)
                          .order_by('nutriscore').values('name', 'category', 'img_url', 'pk')[:1])
        if search_product:
            products = (Product.objects.filter(category__id=search_product[0]['category'])
                        .order_by('nutriscore', 'popularity').values('name', 'nutriscore', 'pk', 'img_url')[:12])
            search_product_status = True
            search_product = search_product[0]
        else:
            products = []
            search_product_status = False
            search_product = {'input': input}

    # return results template with substitute liste as results
    return render(request, 'openfoodfacts/results.html',
                  {'status': search_product_status, 'search': search_product, 'results': products})


def product_detail(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
    except Exception:
        raise Http404

    return render(request, 'openfoodfacts/detail.html', {'result': product})

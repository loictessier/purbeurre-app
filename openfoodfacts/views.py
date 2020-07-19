from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.db.models import Avg
from django.db.models.functions import Coalesce

from .models import Product
from user.models import Profile

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


def results_with_filter(request, search_input):
    if request.method == "POST":
        rating = request.POST['rating-filter']
        request.method = "GET"
        request.GET = request.GET.copy()
        request.GET['search_input'] = search_input

    return results(request, rating)


def results(request, rating_filter=0):
    if request.method == "GET":
        # search for substitutes
        input = request.GET['search_input']
        # remove [] part
        input = re.sub(r'\[.*$', '', input).strip()
        # search substitute
        search_product = (Product.objects.filter(name__icontains=input)
                          .order_by('nutriscore').values('name', 'category', 'img_url', 'pk')[:1])
        if search_product:
            products = (Product.objects.annotate(avg_rating=Coalesce(Avg('ratingproduct__rating'), 0))
                        .filter(category__id=search_product[0]['category'], avg_rating__gte=rating_filter)
                        .order_by('-avg_rating', 'nutriscore', 'popularity').values('name', 'nutriscore', 'pk', 'img_url', 'avg_rating')[:12])
            search_product_status = True
            search_product = search_product[0]
        else:
            products = []
            search_product_status = False
            search_product = {'input': input}

    # return results template with substitute liste as results
    return render(request, 'openfoodfacts/results.html',
                  {'status': search_product_status, 'search': search_product, 'results': products, 'rating_filter': rating_filter})


def product_detail(request, product_id):
    try:
        product = Product.objects.annotate(avg_rating=Avg('ratingproduct__rating')).get(pk=product_id)
        if request.user.is_authenticated:
            current_profile = Profile.objects.get(user=request.user)
            rating_product = current_profile.ratingproduct_set.filter(product=product)
            if rating_product:
                product.rating = rating_product[0].rating
            else:
                product.rating = 0
    except Exception:
        raise Http404

    return render(request, 'openfoodfacts/detail.html', {'result': product})


from django.shortcuts import render
from django.http import HttpResponse

from .models import Product, Category

import json
import re


# Create your views here.
def index(request):
    return render(request, 'openfoodfacts/index.html', { 'header': True })

def get_products(request):
    # request.get => request.GET.get("term")
    # recherche des noms (+[note]) qui contiennent term (django orm) order (note_nutritionnelle/desc) + limit
    # return json avec les noms filtrés
    if request.is_ajax():
        q = request.GET.get('term', '')
        products = Product.objects.filter(name__icontains=q).order_by('-nutriscore','-popularity')[:5]
        results = []
        for pr in products:
            product_json = {}
            product_json['label'] = pr.name + ' [' + pr.nutriscore + '] '
            product_json['id'] = pr.id
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def results(request):
    if request.method == "GET":
        #search for substitutes
        input = request.GET['search_input']
        # remove la partie crochet du nom
        input = re.sub('\[.*$', '', input)
        # à partir du produit recherché s'il n'est pas null recherche des meilleurs substituts pour sa catégorie
        search_product = Product.objects.filter(name__icontains=input).order_by('nutriscore').values('name','category', 'img_url')[:1]
        if search_product:
            # recherche par nom (cas possible ou aucune suggestion n'est utilisée)  
            products = Product.objects.filter(category__id=search_product[0]['category']).order_by('nutriscore', 'popularity').values('name', 'nutriscore', 'pk', 'img_url')[:12]
            search_product_status = True
            search_product = search_product[0]
        else:
            products = []
            search_product_status = False
            search_product = {}
            # redirect to search form 
    
    # return results template with substitute liste as results
    return render(request, 'openfoodfacts/results.html', {'status': search_product_status,'search': search_product, 'results': products})


def product_detail(request, product_id):
    if not product_id:
        raise Http404

    product = Product.objects.get(pk=product_id)

    return render(request, 'openfoodfacts/detail.html', {'result': product})

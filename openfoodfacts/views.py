from django.shortcuts import render
from django.http import HttpResponse

from .models import Product

import json


# Create your views here.
def index(request):
    return render(request, 'index.html')

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
        # recherche par nom (cas possible ou aucune suggestion n'est utilisée)
        # results = Product.objects.filter()
        pass
    
    # return results template with substitute liste as results
    return render(request, 'results.html', { 'results': input })
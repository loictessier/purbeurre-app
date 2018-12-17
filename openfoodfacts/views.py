from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def autocomplete(request):
    # request.get => request.GET.get("term")
    # recherche des noms (+[note]) qui contiennent term (django orm) order (note_nutritionnelle/desc) + limit
    # return json avec les noms filtrés
    pass

def search_substitute(request):
    if request.method == "POST":
        #search for substitutes
        pass
    
    # return results template with substitute liste as results
    return render(request, 'results.html')

def results(request):
    return render(request, 'results.html')
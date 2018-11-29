from django.shortcuts import render

# Create your views here.
def search_substitute(request):
    if request.method == "POST":
        #search for substitutes
        pass
    
    # return results template with substitute liste as results
    return(request, 'results.html')
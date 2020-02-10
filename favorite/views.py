from django.shortcuts import render
from user.models import Profile
from .models import Favorite
from openfoodfacts.models import Product
from django.http import JsonResponse

# Create your views here.
def favorites(request):
    if request.method == "GET":
        current_profile = Profile.objects.get(user=request.user)
        favorites = current_profile.favorite_set.all()
        if favorites:
            status = True
        else:
            status = False

    return render(request, 'favorite/favorites.html', { 'status': status, 'favorites': favorites })


def add_favorite(request, substitute_product_id, origin_product_id):
    if request.user.is_authenticated:
        current_profile = Profile.objects.get(user=request.user)
        substitute_product = Product.objects.get(id=substitute_product_id)
        origin_product = Product.objects.get(id=origin_product_id)

        try:
            favorite = Favorite(profile=current_profile, product=substitute_product, origin_product=origin_product)
            favorite.save()
            status = 200
            res = "Le produit à été ajouté aux favoris."
        except:    
            status = 500
            res = "Erreur lors de l'ajout du favoris."
    else:
        status = 401
        res = "Erreur d'authentification"

    return JsonResponse({'status':status, 'message':res})
from django.shortcuts import render
from user.models import Profile
from .models import Favorite
from openfoodfacts.models import Product
from django.http import JsonResponse
from django.urls import reverse


# Create your views here.
def favorites(request):
    status = False
    favorites = {}
    if request.method == "GET":
        if request.user.is_authenticated:
            current_profile = Profile.objects.get(user=request.user)
            favorites = current_profile.favorite_set.all()
            if favorites:
                status = True

    return render(request, 'favorite/favorites.html', {'status': status, 'favorites': favorites})


def add_favorite(request, substitute_product_id):
    if request.user.is_authenticated:
        current_profile = Profile.objects.get(user=request.user)

        try:
            substitute_product = Product.objects.get(id=substitute_product_id)
            favorite = Favorite(profile=current_profile, product=substitute_product)
            favorite.save()
            status = 200
            res = "Le produit a été ajouté aux favoris."
        except Exception:
            status = 500
            res = "Erreur lors de l'ajout du favoris."
    else:
        status = 401
        res = "Erreur d'authentification"

    url = reverse("favorite:remove_favorite", kwargs={'product_id': substitute_product_id})

    return JsonResponse({'status': status, 'message': res, 'replace_url': url, 'action': 'remove'})


def remove_favorite(request, product_id):
    if request.user.is_authenticated:
        current_profile = Profile.objects.get(user=request.user)
        try:
            favorite_product = Product.objects.get(id=product_id)
            favorites = current_profile.favorite_set.filter(product=favorite_product)
            favorites.delete()
            status = 200
            res = "Le produit a été retiré des favoris"
        except Exception:
            status = 500
            res = "Erreur lors de la suppression du favoris."
    else:
        status = 401
        res = "Erreur d'authentification"

    url = reverse("favorite:add_favorite", kwargs={'substitute_product_id': product_id})

    return JsonResponse({'status': status, 'message': res, 'replace_url': url, 'action': 'save'})

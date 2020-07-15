from django.shortcuts import render, redirect
from django.http import JsonResponse

from user.models import Profile
from rating.models import RatingProduct
from openfoodfacts.models import Product

# Create your views here.
def post_rating_product(request, product_id):
    if request.method == 'POST':
        rating = request.POST['rating-product']
        if rating != "0":
            add_rating_product(request, product_id, rating)
        else:
            remove_rating_product(request, product_id)

    return redirect('openfoodfacts:detail', product_id=product_id)

def add_rating_product(request, product_id, rating):
    if request.user.is_authenticated:
        current_profile = Profile.objects.get(user=request.user)

        try:
            product = Product.objects.get(id=product_id)
            rating, created = RatingProduct.objects.update_or_create(
                profile=current_profile,
                product=product,
                defaults={'rating': rating})
            status = 200
            res = "La note a été créée / mise à jour"
        except Exception:
            status = 500
            res = "Erreur lors de la création / mise à jour de la note"
    else:
        status = 401
        res = "Erreur d'authentification"

    return JsonResponse({'status': status, 'message': res})


def remove_rating_product(request, product_id):
    if request.user.is_authenticated:
        current_profile = Profile.objects.get(user=request.user)
        try:
            rated_product = Product.objects.get(id=product_id)
            rating_product = current_profile.ratingproduct_set.filter(product=rated_product)
            rating_product.delete()
            status = 200
            res="La note a été supprimée"
        except Exception:
            status = 500
            res = "Erreur lors de la suppression de la note"
    else:
        status = 401
        res = "Erreur d'authentification"

    return JsonResponse({'status': status, 'message': res})

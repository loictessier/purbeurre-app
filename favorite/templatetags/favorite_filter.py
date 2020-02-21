from django import template
from user.models import Profile
from favorite.models import Favorite
from openfoodfacts.models import Product

register = template.Library()

@register.filter(name='check_product_favorite')
def check_product_favorite(product_id, user):
    profile = Profile.objects.get(user=user)
    return profile.favorite_set.filter(product=Product.objects.get(id=product_id)).exists()

    
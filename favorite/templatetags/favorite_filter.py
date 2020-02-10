from django import template
from user.models import Profile
from favorite.models import Favorite

register = template.Library()

@register.filter(name='check_product_favorite')
def check_product_favorite(product, user):
    profile = Profile.objects.get(user=user)
    return profile.favorite_set.filter(product=product['pk']).exists()

    
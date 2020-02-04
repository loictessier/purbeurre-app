from django.shortcuts import render
from user.models import Profile

# Create your views here.
def favorites(request):
    current_profile = Profile.objects.get(user=request.user)
    favorites = current_profile.favorite_set.all()
    if favorites:
        status = True
    else:
        status = False

    return render(request, 'favorite/favorites.html', { 'status': status, 'favorites': favorites })

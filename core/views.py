from django.shortcuts import render

def legal_notice(request):
    return render(request, 'core/legals.html', { 'status': False }) 
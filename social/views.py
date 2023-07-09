from django.shortcuts import render

# Create your views here.
def handler404(request, exception=None):
    return render(request, '404.html', status=404)
    
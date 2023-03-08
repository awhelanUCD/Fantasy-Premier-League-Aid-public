from django.shortcuts import render

# Create your views here.
from home_page.models import Features

def home_page(request):
    features = Features.objects.all()
    context = {
        'features': features,
    }
    return render(request, 'home_page/home_page.html', context)
# Create your views here.

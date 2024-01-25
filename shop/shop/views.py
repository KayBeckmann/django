from django.shortcuts import render
from . models import *

def shop(request):
  # ctx steht für CONTEXT
  artikels = Artikel.objects.all()
  ctx = {'artikels':artikels}
  return render(request, 'shop/shop.html', ctx)

def warenkorb(request):
  return render(request, 'shop/warenkorb.html')

def kasse(request):
  return render(request, 'shop/kasse.html')
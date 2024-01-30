from django.shortcuts import render
from django.http import JsonResponse
from . models import *

def shop(request):
  # ctx steht für CONTEXT
  artikels = Artikel.objects.all()
  ctx = {'artikels':artikels}
  return render(request, 'shop/shop.html', ctx)

def berechnungBestellung(request):
  if request.user.is_authenticated:
    kunde = request.user.kunde
    bestellung, created = Bestellung.objects.get_or_create(kunde = kunde, erledigt = False)
    artikels = bestellung.bestellteartikell_set.all()
  else:
    artikels = []
    bestellung = []
    
  ctx = {"artikels": artikels, "bestellung":bestellung}
  return ctx

def warenkorb(request):
  ctx = berechnungBestellung(request)
  return render(request, 'shop/warenkorb.html', ctx)

def kasse(request):
  ctx = berechnungBestellung(request)
  return render(request, 'shop/kasse.html', ctx)

def artikelbackend(request):
  return JsonResponse("Artikel hinzugefuegt", safe=False)
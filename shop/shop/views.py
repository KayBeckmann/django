from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe
import json
from . models import *
import uuid
from paypal.standard.forms import PayPalPaymentsForm

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
  daten = json.loads(request.body)
  artikelId = daten['artikelId']
  action = daten['action']
  kunde = request.user.kunde
  artikel = Artikel.objects.get(id=artikelId)
  bestellung, created = Bestellung.objects.get_or_create(kunde = kunde, erledigt=False)
  bestellteArtikell, created = BestellteArtikell.objects.get_or_create(bestellung=bestellung, artikel=artikel)
  
  if action == 'bestellen':
    bestellteArtikell.menge = bestellteArtikell.menge + 1
    messages.success(request, "Artikel wurde zum Warenkorb hinzugefügt.")
  elif action == 'entfernen':
    bestellteArtikell.menge = bestellteArtikell.menge - 1
    messages.warning(request, "Artikel wurde aus dem Warenkorb entfernt.")
      
  bestellteArtikell.save()
  
  if bestellteArtikell.menge <= 0:
    bestellteArtikell.delete()
  
  return JsonResponse("Artikel hinzugefuegt", safe=False)

def loginSeite(request):
  if request.method == 'POST':
    benutzername = request.POST['benutzername']
    passwort = request.POST['passwort']
    
    benutzer = authenticate(request, username=benutzername, password=passwort)
    
    if benutzer is not None:
      login(request, benutzer)
      return redirect('shop')
    else:
      messages.error(request, "Fehler beim Login.")
      
  seite = "login"
  ctx = {"seite":seite}
  return render(request, 'shop/login.html', ctx)

def logoutSeite(request):
  logout(request)
  return redirect('shop')

def regSeite(request):
  seite = "reg"
  form = UserCreationForm
  
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      benutzer = form.save(commit=False)
      benutzer.save()
      
      kunde = Kunde(name=request.POST['username'], benutzer=benutzer)
      kunde.save()
      bestellung = Bestellung(kunde=kunde)
      bestellung.save()
      
      login(request, benutzer)
      return redirect('shop')
    else:
      messages.error(request, "Fehlerhafte Eingabe.")
  
  ctx = {'form': form, 'seite':seite}
  return render(request, 'shop/login.html', ctx)

def bestellen(request):
  auftrags_id = uuid.uuid4()
  daten = json.loads(request.body)
  
  if request.user.is_authenticated:
    kunde = request.user.kunde
    bestellung, created = Bestellung.objects.get_or_create(kunde = kunde, erledigt = False)
    gesamtpreis = float(daten['benutzerdaten']['gesamtpreis'])
    bestellung.auftrags_id = auftrags_id
    bestellung.erledigt = True
    bestellung.save()
    
    Adresse.objects.create(
      kunde = kunde,
      bestellung = bestellung,
      strasse = daten['lieferadresse']['adresse'],
      plz = daten['lieferadresse']['plz'],
      stadt = daten['lieferadresse']['stadt'],
      land = daten['lieferadresse']['land']
    )

    paypal_dict = {
        "business": "sb-347tah29743032@business.example.com",
        "amount": gesamtpreis,
        "item_name": auftrags_id,
        "invoice": auftrags_id,
        "currency_code": "EUR",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('shop')),
        "cancel_return": request.build_absolute_uri(reverse('shop')),
    }

    paypalform = PayPalPaymentsForm(initial = paypal_dict)

  else:
    print("nicht eingeloggt!")
  
  auftragsUrl = str(auftrags_id)
  messages.success(request, mark_safe("Danke für Ihre <a href='/bestellung/"+auftragsUrl+"'>Bestellung</a>.</br>Jetzt bezahlen: "+paypalform.render()))
  return JsonResponse('Bestellung erfolgreich', safe=False)

@login_required(login_url = 'login')
def bestellung(request, id):
  bestellung = Bestellung.objects.get(auftrags_id = id)
  print(bestellung)
  if bestellung: # and str(request.user) == str(bestellung.kunde):
    bestellung = Bestellung.objects.get(auftrags_id=id)
    artikels = bestellung.bestellteartikell_set.all()
    ctx = {'artikels':artikels, 'bestellung':bestellung}
    return render(request, 'shop/bestellung.html', ctx)
  else:
    return render(request, 'shop/404.html')
  
def fehler404(request, exception):
  return render(request, 'shop/404.html')
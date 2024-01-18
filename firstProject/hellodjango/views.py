from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

#View
def hallo(req):
    return JsonResponse('Hallo Welt!', safe=False)

def start(req):
  return JsonResponse('Startseite', safe=False)
from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

#View
def hallo(req):
    return JsonResponse('Hallo Welt!', safe=False)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hallo)
]

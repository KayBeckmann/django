from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('warenkorb/', views.warenkorb, name='warenkorb'),
    path('kasse/', views.kasse, name='kasse'),
    path('artikel_backend/', views.artikelbackend, name='artikel_backend'),
    path('login/', views.loginSeite, name='login'),
    path('logout/', views.logoutSeite, name='logout'),
    path('reg/', views.regSeite, name='reg'),
    path('bestellen/', views.bestellen, name='bestellen'),
    path('bestellung/<uuid:id>', views.bestellung, name='bestellung'),
]


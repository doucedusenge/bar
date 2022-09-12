from django.contrib import admin
from django.db import router
from django.urls import path,include
from rest_framework import routers
from .views import *

router= routers.DefaultRouter()
router.register("produit",ProduitViewSet)
router.register("achat",AchatViewSet)
router.register("vente",VenteViewSet)



urlpatterns = [
    path('', include(router.urls)),
    path('api_auth', include('rest_framework.urls'))
    
]
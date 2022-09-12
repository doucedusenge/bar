from argparse import Action
from itertools import count
from django.shortcuts import render
from urllib import response
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import *
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from django.db.models import Sum
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class ProduitViewSet(viewsets.ModelViewSet):
    authentication_classes=[SessionAuthentication]
    permission_classes= [AllowAny]
    queryset=Produit.objects.all()
    serializer_class=ProduitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nom_produit']


class AchatViewSet(viewsets.ModelViewSet):
    authentication_classes=[SessionAuthentication]
    permission_classes= [AllowAny]
    queryset=Achat.objects.all()
    serializer_class=AchatSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_fields =['quantite']

    @action(detail=False,methods=['get'],url_path=r"tot_achat",url_name=r"tot_achat")
    def get_achat(self,request):
        achat=Achat.objects.filter(prix__gte=0).aggregate(Sum("prix")).get("prix__sum")
        return Response({"la_somme_est:":achat})

        
    @action(detail=False,methods=['get'],url_path=r'somme',url_name=r'somme')   
    def get_quantite(self,request):
        quantite=Achat.objects.filter(quantite__gte=0).aggregate(Sum('quantite')).get('quantite__sum')
        return Response({ 'somm':quantite})

    @action(detail=False,methods=['get'],url_path=r'prix',url_name=r'prix')
    def get_prix(self,request):
        prix=Achat.objects.filter(prix__gte=0)
        quantite=Achat.objects.filter(quantite__gte=0)
        prix.prix *=quantite.prix
        prix.save()
        return Response({'montant egal':prix})

    def create(self, request):
        data=request.data
        produit_obj=Produit.objects.get(id=data["produit"])
        achat_obj=Achat (
            produit=produit_obj,
            prix=int(data["prix"]),
            quantite=int(data["quantite"])
            ) 
        achat_obj.save()
        produit_obj.quantite +=int(data["quantite"])
        produit_obj.save()
        return Response(200)

class VenteViewSet(viewsets.ModelViewSet):
    authentication_classes=[SessionAuthentication]
    permission_classes=[AllowAny]
    queryset=Vente.objects.all()
    serializer_class=VenteSerializer  
    filter_backends=[DjangoFilterBackend]
    filterset_fields= ['quantite']


    
    @action(detail=False,methods=['get'],url_path=r'vente_tot',url_name=r'vente_tot')
    def get_vente(self,request):
        vente=Vente.objects.filter(prix__gte=0).aggregate(Sum("prix")).get("prix__sum")
        return Response({"la_somme_est": vente},200)

    @action(detail=False,methods=['get'],url_path=r'benefice',url_name=r'benefice')   
    def get_benefice(self,request):
        benefice_com=[]
        benefice_ven=[]
        produit=Produit.objects.filter('prix__gte=0')
        somme=0
        for p in produit:
            vente=Vente.objects.filter(produit.p).aggregate(Sum("prix")).get("prix__sum")
            achat=Achat.objects.filter(produit.p).aggregate(Sum("prix")).get("prix__sum")
            benefice_com.append(vente)
            benefice_ven.append(achat)
            benefice_ven.append(vente-achat)
        
        for x in benefice_ven:
            if(x):
                somme+=x  
            return  Response({'benefice':somme})
    def create(self, request):
        data=request.data
        produit_obj=Produit.objects.get(id=data['produit'])
        vente_obj=Vente(
            produit=produit_obj,
            quantite= int(data["quantite"]),
            prix=int(data["prix"])
        )
        vente_obj.prix *= int(data["quantite"])
        vente_obj.save()
        produit_obj.quantite -=int(data["quantite"])
        produit_obj.save()

        return Response({'somme':vente_obj.prix},200)
    
    

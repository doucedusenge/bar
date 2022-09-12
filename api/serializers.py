from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from .models import *


class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model=Produit
        fields="__all__"

class  AchatSerializer(serializers.ModelSerializer):
    class Meta:
        model=Achat
        fields="__all__"

        def to_representation(self, instance):
            representation=super().to_representation(instance)
            representation["produit"]=ProduitSerializer(instance.produit,many=False).data
            produit=ProduitSerializer(instance.produit,many=False).data
            representation["produit"]=ProduitSerializer(instance.produit,many=False).data

            return  representation


class VenteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vente
        fields="__all__"         

   

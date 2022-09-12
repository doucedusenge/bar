from tkinter import CASCADE
from django.db import models

# Create your models here.


class Produit(models.Model):
    id=models.BigAutoField(primary_key=True)
    nom_produit=models.CharField(max_length=50)
    quantite=models.IntegerField(default=0)
    prix=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nom_produit

class Achat(models.Model):
    id=models.AutoField(primary_key=True)
    produit=models.ForeignKey(Produit,on_delete=models.CASCADE)
    prix=models.PositiveIntegerField(default=0)
    quantite=models.PositiveIntegerField(default=0) 

class Vente(models.Model):
    id=models.AutoField(primary_key=True)
    produit=models.ForeignKey(Produit,on_delete=models.CASCADE)
    prix=models.PositiveIntegerField(default=0)
    quantite=models.PositiveIntegerField(default=0) 


           

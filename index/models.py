from django.db import models
import datetime
import os
from django.contrib.auth.models import User


def getFileName(requset,filename): #to get the date and time for the name for the image
    now_time=datetime.datetime.now().strftime("%y%m%d%H:%M:%S")
    new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)

class Catagory(models.Model): #to get the catagory details llike phone,book,etc..
    name= models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-hidden,1-show")
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):      
        return self.name
    
class Product(models.Model): #to add the products in the catogory that that added
    Catagory=models.ForeignKey(Catagory,on_delete=models.CASCADE)
    name= models.CharField(max_length=150,null=False,blank=False)
    vendor= models.CharField(max_length=150,null=False,blank=False)
    Product_image=models.ImageField(upload_to=getFileName,null=True,blank=True)
    quantity= models.IntegerField(null=False,blank=False)
    original_price= models.FloatField(null=False,blank=False)
    selling_price=models.FloatField(null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-show,1-hidden")
    trending=models.BooleanField(default=False,help_text="0-show,1-hidden")
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Cart(models.Model): #to add the products in the cart 
    user=models. ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey (Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False, blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    @property #to get the total cost of the cart products
    def total_cost(self):
        return self.product_qty*self.product.selling_price 
    
class Favourite(models.Model): #to add the favourites of the products
    user=models.ForeignKey (User,on_delete=models.CASCADE)
    product=models.ForeignKey (Product,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

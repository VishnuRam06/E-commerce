from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from .form import RegisterForm
from django.contrib.auth import login,logout,authenticate
import json


def home(request): #redirect to the home page
    product= Product.objects.filter(trending=0)
    return render(request,'index/index.html',context={"products":product})

def logout_page(request): #to logout the user
    if request.user.is_authenticated: #to check the user is login or not
        logout(request) 
        messages.success(request,"Logout successfully")
        return redirect('/')


def login_page(request):  #to login the user 
    if request.user.is_authenticated: #to check wether the user is already login or not 
        return redirect('/')
    else:   #if not login the get the the username and password and authenticate
        if request.method == "POST":
            name=request.POST.get('username')
            pwd=request.POST.get('Password')
            user=authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user) #if the username and password is crorrect then get notification
                messages.success(request,"Login successfully")
                return redirect('/')
            else:  #else it will show the invalid message
                messages.success(request,"Invalid Username or Password")
                return redirect('/login')
        return render(request,'index/login.html')

def register(request):
    form=RegisterForm() #created the UserCreationForm in the form.py we have imported that for geting the registrastion details
    if request.method == "POST":
        form=RegisterForm(request.POST) #to save the details of UserCreationForm
        if form.is_valid():
            form.save()
            messages.success(request,"Registration successful Login Now..!")
            return redirect('/login')
    return render(request,'index/register.html',context={"form":form}) #it will return to the registrastion page

def collections(request):  # to filter the catogry
    catagory= Catagory.objects.filter(status=1)
    return render(request,'index/collections.html',context={"catagory":catagory})

def collections_Product(request,name): # to filter the products by the catogry name 
    if(Catagory.objects.filter(name=name,status=1)): #to check the paroduct can be shown in the display or not
        products=Product.objects.filter(Catagory__name=name)
        return render(request,'index/products.html',context={"products":products,"Catagory_list":name} )
    else:
        messages.warning(request,"no products found")
        return redirect('collections')
    
def Product_details(request,catogoryname,productname): # to filter the products details by catogory and product name 
    if(Catagory.objects.filter(name=catogoryname,status=1)): #to check whether the catogory to show or not
        if(Product.objects.filter(name=productname,status=0)): #to check whether the product to show or not
            products=Product.objects.filter(name=productname,status=0).first()
            return render(request,'index/products_details.html',context={"products":products} )
        else:
            messages.error(request,"no such product found")
            return redirect(collections)
    else:
        messages.error(request,"no such catagory found")
        return redirect(collections)
    

def add_to_cart(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest': # to check the http request from the frontend in product details page
        if request.user.is_authenticated:
            data = json.loads(request.body) #to get in json value
            product_qty = data.get('product_qty') #var is to get the no of quatity
            product_id = data.get('pid') #var is to get the product id
            product_status = Product.objects.get(id=product_id) # to check whether the product is available or not
            if product_status:
                if Cart.objects.filter(user=request.user.id, product_id=product_id): #if available then to check already in the cart database
                     return JsonResponse({'status': 'Product Already in Cart'}, status=200)
                else:
                    if product_status.quantity >= product_qty:
                     Cart.objects.create(user_id=request.user.id, product_id=product_id, product_qty=product_qty)
                     return JsonResponse({'status': 'Product Added to Cart'}, status=200)
                    else:
                        return JsonResponse({'status': 'Product Stock Not Available'}, status=200)
        else:
            return JsonResponse({'status': 'Login to Add Cart'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)
    
def cart(request):
    if request.user.is_authenticated: #to checl whwther the user is authenticated or not
        cart=Cart.objects.filter(user=request.user) #to check the user id in the cart to get the add to cart details of the particular user
        return render(request,"index/cart.html",{"cart":cart})
    else:
        return redirect('/')

def cart_remove(request,itemid): #to get the the item id to remove the particular product to remove from the add to cart
    cartitem=Cart.objects.get(id=itemid) #to get whether the particular product in the cart database and delete for the particular user
    cartitem.delete() 
    return redirect('cart')
    

def favourite(request):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest': # to check the http request from the frontend in product details page
        if request.user.is_authenticated:
            data = json.loads(request.body)  #to get in json value
            product_id = data.get('pid') #var is to get the product id
            Favourite.objects.create(user_id=request.user.id, product_id=product_id) # to add the products to the favourite
            return JsonResponse({'status': 'Products Added to favourite'}, status=200) 
        else:
            return JsonResponse({'status': 'Login to Add favourite'}, status=200)
    else:
        return JsonResponse({'status': 'Invalid Access'}, status=200)
    
def fav_page(request):
    if request.user.is_authenticated:
        favourite=Favourite.objects.filter(user=request.user) #to get the particular user id's favourite products 
        return render(request,"index/favourite.html",{"favourite":favourite})
    else:
        return redirect('/')

def fav_remove(request,itemid):
    favitem=Favourite.objects.get(id=itemid) #to remove the particular user id's particular favourite products
    favitem.delete()
    return redirect('fav_page')
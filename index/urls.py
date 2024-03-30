from django.contrib import admin
from django.urls import path
from .import views as v1

urlpatterns = [
    path('',v1.home, name='home' ),
    path('register/',v1.register,name='register' ),
    path('login',v1.login_page,name='login' ),
    path('logout/',v1.logout_page,name='logout' ),
    path('collections/',v1.collections,name='collections' ),
    path('collections_Product/<str:name>',v1.collections_Product,name='collections_Product' ),
    path('collections/<str:catogoryname>/<str:productname>/',v1.Product_details,name='Product_details'),
    path('addtocart',v1.add_to_cart,name='addtocart' ), # / in the html file
    path('cart/',v1.cart,name='cart' ),
    path('cartremove/<str:itemid>', v1.cart_remove , name='cartremove' ),
    path('fav',v1.favourite,name='fav' ), # / in the html file
    path('fav_page',v1.fav_page,name='fav_page' ),
    path('fav_remove/<str:itemid>', v1.fav_remove , name='fav_remove' ),
]

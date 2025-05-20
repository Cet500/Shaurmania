from django.urls import path
from . import views


urlpatterns = [

    path ('', views.index, name = 'index'),

    # CATALOG ==============================================
    path ('catalog', views.catalog, name = 'catalog'),
    path ('product/<int:product_id>', views.product, name = 'product'),
    path ('search',  views.search,  name = 'search'),
    path ('cart',    views.cart,    name = 'cart'),

    # LOGIN SYSTEM =========================================
    path ('login',  views.login,  name = 'login'),
    path ('reg',    views.reg,    name = 'reg'),
    path ('logout', views.logout, name = 'logout' ),

    # USERS ================================================
    path ('user_private', views.user_private, name = 'user_private'),
    path ('user_public',  views.user_public,  name = 'user_public'),

    # MISC =================================================
    path ('about',    views.about,    name = 'about'),
    path ('address',  views.address,  name = 'address'),
    path ('feedback', views.feedback, name = 'feedback'),
    path ('licenses', views.licenses, name = 'licenses'),
    path ('stocks',   views.stocks,   name = 'stocks'),

]

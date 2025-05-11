from django.urls import path
from . import views


urlpatterns = [
    path ('about', views.about, name = 'about'),
    path ('address', views.address, name = 'address'),
    path ('cart', views.cart, name = 'cart'),
    path ('catalog', views.catalog, name = 'catalog'),
    path ('feedback', views.feedback, name = 'feedback'),
    path ('', views.index, name = 'index'),
    path ('licenses', views.licenses, name = 'licenses'),
    path ('login', views.login, name = 'login'),
    path ('product/<int:product_id>', views.product, name = 'product'),
    path ('reg', views.reg, name = 'reg'),
    path ('sales', views.sales, name = 'sales'),
    path ('search', views.search, name = 'search'),
    path ('user_private', views.user_private, name = 'user_private'),
    path ('user_public', views.user_public, name = 'user_public'),
    path ('logout', views.logout_jopa, name = 'logout')
]
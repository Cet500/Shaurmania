from django.urls import path
from . import views


urlpatterns = [

    path ('', views.index, name = 'index'),

    # CATALOG ==============================================
    path ('catalog', views.catalog, name = 'catalog'),
    path ('product/<slug:slug>', views.product, name = 'product'),
    path ('search',  views.search,  name = 'search'),

    # LOGIN SYSTEM =========================================
    path ('login',  views.login,  name = 'login'),
    path ('reg',    views.reg,    name = 'reg'),
    path ('logout', views.logout, name = 'logout' ),

    # USER =================================================
    path ('user/<str:username>', views.user, name = 'user'),
    path ('profile_closed',      views.user_closed, name = 'user_closed'),

    # MISC =================================================
    path ('about',             views.about,    name = 'about'),
    path ('address',           views.address,  name = 'address'),
    path ('feedback',          views.feedback, name = 'feedback'),
    path ('licenses',          views.licenses, name = 'licenses'),
    path ('stocks',            views.stocks,   name = 'stocks'),
    path ('stock/<slug:slug>', views.stock,    name = 'stock'),

    # DEV ==================================================
    path( 'dev', views.dev, name = 'dev' ),

    # ADMIN ================================================
    path('admin/factories',            views.admin_factories,        name = 'admin_factories'),
    path('admin/factories/<str:name>', views.admin_factory_generate, name = 'admin_factory_generate'),
]

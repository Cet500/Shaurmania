from django.urls import path
from . import views as v


urlpatterns = [

    path ('', v.index, name = 'index'),

    # CATALOG ==============================================
    path ('catalog',             v.catalog, name = 'catalog'),
    path ('product/<slug:slug>', v.product, name = 'product'),
    path ('search',              v.search,  name = 'search'),

    # LOGIN SYSTEM =========================================
    path ('login',  v.login,  name = 'login'),
    path ('reg',    v.reg,    name = 'reg'),
    path ('logout', v.logout, name = 'logout' ),

    # USER =================================================
    path ('user/<str:username>', v.user,        name = 'user'),
    path ('profile_closed',      v.user_closed, name = 'user_closed'),

    # DOCS =================================================
    path( 'docs',                v.docs,           name = 'docs' ),
    path( 'docs/privacy_policy', v.privacy_policy, name = 'privacy_policy' ),
    path( 'docs/user_agreement', v.user_agreement, name = 'user_agreement' ),
    path( 'docs/user_consent',   v.user_consent,   name = 'user_consent' ),
    path( 'docs/license',        v.license,        name = 'license' ),
    path( 'docs/add_license_1',  v.add_license_1,  name = 'add_license_1' ),
    path( 'docs/san_rules',      v.san_rules,      name = 'san_rules' ),
    path( 'docs/codex',          v.codex,          name = 'codex' ),
    path( 'docs/decree',         v.decree,         name = 'decree' ),

    # MISC =================================================
    path ('about',             v.about,    name = 'about'),
    path ('address',           v.address,  name = 'address'),
    path ('feedback',          v.feedback, name = 'feedback'),
    path ('stocks',            v.stocks,   name = 'stocks'),
    path ('stock/<slug:slug>', v.stock,    name = 'stock'),

    # DEV ==================================================
    path( 'dev', v.dev, name = 'dev' ),

    # ADMIN ================================================
    path('admin/factories',            v.admin_factories,        name = 'admin_factories'),
    path('admin/factories/<str:name>', v.admin_factory_generate, name = 'admin_factory_generate'),
]

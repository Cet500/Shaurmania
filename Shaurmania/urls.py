# ----------------------------------------- #
# URL configuration for Shaurmania project. #
# ----------------------------------------- #

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from main import views as main_views


urlpatterns = [
    path( 'admin-panel/', admin.site.urls ),
    path( '', include( 'main.urls' ) ),
    path( 'cart/', include( 'cart.urls' ) ),

    path( 'errors/400/', main_views.error_400, {'exception': Exception('Bad Request')},       name = 'errors_400' ),
    path( 'errors/403/', main_views.error_403, {'exception': Exception('Permission Denied')}, name = 'errors_403' ),
    path( 'errors/404/', main_views.error_404, {'exception': Exception('Page not Found')},    name = 'errors_404' ),
    path( 'errors/500/', main_views.error_500, name = 'errors_500' )
]

handler400 = 'main.views.error_400'
handler403 = 'main.views.error_403'
handler404 = 'main.views.error_404'
handler500 = 'main.views.error_500'

if settings.DEBUG:
    urlpatterns += static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT )

    if settings.IS_DDT_ACTIVE:
        from debug_toolbar.toolbar import debug_toolbar_urls
        import mimetypes

        mimetypes.add_type( "application/javascript", ".js", True )
        urlpatterns += debug_toolbar_urls()

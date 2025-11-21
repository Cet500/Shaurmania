from django.urls import path
from . import views as v


urlpatterns = [
    # API ==================================================
    path('admin/factories',            v.admin_factories,        name = 'admin_factories'),
    path('admin/factories/<str:name>', v.admin_factory_generate, name = 'admin_factory_generate'),
]

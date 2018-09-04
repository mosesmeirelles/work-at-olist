from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Phone Bills API",
      default_version='v1',
      description="It implements an REST API application that receives call detail records and "
                  "calculates monthly bills for a given telephone number.",
      contact=openapi.Contact(email="moisesmeirelles@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(('phonebillsapi.api.urls', 'api'), namespace='api')),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='docs'),
]

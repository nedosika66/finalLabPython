from django.urls import path
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('music_app.urls_api')),
    path('web/', include('web.urls'))
]
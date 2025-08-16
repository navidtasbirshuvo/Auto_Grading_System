from django.contrib import admin
from django.urls import path, include
from authentication.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('auth/', include('authentication.urls')),
    path('', include('frontend.urls')),
    path('core/', include('core.urls')),
]

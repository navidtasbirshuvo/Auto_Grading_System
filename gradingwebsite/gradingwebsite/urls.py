from django.contrib import admin
from django.urls import path, include
from authentication.views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Add login at root level to match frontend expectations
    path('login/', login_view, name='login'),

    # Authentication URLs
    path('auth/', include('authentication.urls')),

    # Add your frontend URLs here (includes dashboards)
    path('', include('frontend.urls')),

    # Core app URLs (exam system)
    path('core/', include('core.urls')),
]

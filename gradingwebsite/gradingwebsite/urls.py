from django.contrib import admin
from django.urls import path, include
from authentication.views import student_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Add your frontend URLs here
    path('', include('frontend.urls')),

    # Example if you have authentication and core apps
    path('auth/', include('authentication.urls')),
    #path('core/', include('core.urls')),
    path('auth/student-dashboard/', student_dashboard, name='student_dashboard')
]

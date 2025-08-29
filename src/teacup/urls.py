"""
URL configuration for teacup project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

def api_root(request):
    """API root endpoint showing available endpoints"""
    return JsonResponse({
        'message': 'Welcome to Teacup Social Media API',
        'version': '1.0.0',
        'endpoints': {
            'users': '/api/v1/users/',
            'posts': '/api/v1/posts/',
            'feed': '/api/v1/feed/',
            'comments': '/api/v1/comments/',
            'admin': '/admin/',
            'api_docs': '/api/docs/',
            'api_schema': '/api/schema/',
            'authentication': '/api/v1/auth/',
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('posts.urls')),
    path('api/v1/', include('feed.urls')),
    
    # Authentication endpoints
    path('api/v1/auth/', include('rest_framework.urls')),
    
    # API documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

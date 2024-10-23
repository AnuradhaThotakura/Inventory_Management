# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ItemViewSet

router = DefaultRouter()
router.register(r'items', ItemViewSet, basename='items')

urlpatterns = [
    path('', include(router.urls)),  # Includes all routes registered with the router
]

from rest_framework.routers import DefaultRouter
from .views import AvailabilityViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('availabilities', AvailabilityViewSet, basename='availability')

urlpatterns = [path('', include(router.urls))]

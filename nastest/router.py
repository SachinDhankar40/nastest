from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'get-info', GetInfoView, basename='get-info')
router.register(r'unpark', UnparkView, basename='unpark')
router.register(r'park', ParkView, basename='park')
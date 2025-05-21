from django.urls import path  
from rest_framework.routers import DefaultRouter  
from .views import PaymentViewSet  


router = DefaultRouter()  
router.register(r'', PaymentViewSet, basename='financial_reporting') 

urlpatterns = router.urls

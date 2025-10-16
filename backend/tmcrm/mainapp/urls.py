from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from django.views.generic import RedirectView
from rest_framework.routers import SimpleRouter
from .views import OrganizationViewSet


router = SimpleRouter()
router.register(r'organizations', OrganizationViewSet, basename='organization')   

                                                                 
urlpatterns = [                                             
    path('', RedirectView.as_view(url="/admin/", permanent=True)),
]

urlpatterns += router.urls

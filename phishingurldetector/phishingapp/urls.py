from django.urls import path
from django.urls import path,include

from . import views

from  phishingapp.views import phishingViewSet
from rest_framework import routers

router = routers.DefaultRouter()

app_name = 'phishingapp'

router.register(r'phishing',phishingViewSet,basename='phishing')


urlpatterns  = [
    path("",views.index,name="index"),
    path('api/',include(router.urls))
]
from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'cycles', views.CyclesLengthViewSet)
router.register(r'temperatures', views.TemperatureViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

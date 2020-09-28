from django.urls import path, include
from rest_framework.routers import DefaultRouter

from servers import views

router = DefaultRouter()
router.register(r"server", views.ServerViewSet)

urlpatterns = [
    path("command", views.CommandAPIView.as_view(), name="Command"),
    path("", include(router.urls)),
]

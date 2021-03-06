from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework.authtoken import views

from .invoxia_view import InvoxiaUpdateBikeLocation
from .views import (
    StationViewSet,
    LoginProviderViewSet,
    MaintenanceViewSet,
    RentViewSet,
    UserDetailsView,
    updatebikelocation,
)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"stations", StationViewSet, basename="station")
router.register(r"rent", RentViewSet, basename="rent")
router.register(r"maintenance", MaintenanceViewSet, basename="maintenance")

urlpatterns = [
    re_path(r"^", include(router.urls)),
    path("bike/updatelocation", updatebikelocation),
    path("bike/invoxia/updatelocation", InvoxiaUpdateBikeLocation),
    path("user", UserDetailsView.as_view()),
    path("config/loginproviders", LoginProviderViewSet.as_view({"get": "list"})),
    path("auth/token", views.obtain_auth_token),
]

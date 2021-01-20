from .invoxia_serializer import InvoxiaLocationTrackerUpdateSerializer
from allauth.socialaccount.models import SocialApp
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from django.utils.timezone import now, timedelta
from preferences import preferences
from rest_framework import exceptions, generics, mixins, status, viewsets
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.decorators import (
    action,
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import (
    SAFE_METHODS,
    AllowAny,
    BasePermission,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler

from bikesharing.models import Bike, Location, LocationTracker, Rent, Station
from cykel.models import CykelLogEntry


@api_view(["POST"])
@permission_classes([AllowAny])
def InvoxiaUpdateBikeLocation(request):
    #device_id = request.data.get("serial")
    someminutesago = now() - timedelta(minutes=15)
    x_api_key = request.META.get('HTTP_X_API_KEY')
    if x_api_key != "7IUpcjcj.fXzNRFtonGiAwLUNzOWMdtY7Q3G7xdqN":
        return Response({"error": "wrong key".format(x_api_key)}, status=400)
    #if not (device_id):
    #    return Response({"error": "serial missing"}, status=400)
    #trackers = LocationTracker.objects.all()
    serializer = InvoxiaLocationTrackerUpdateSerializer(data=request.data, many=True)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    serializer.save()
    #status = serializer.save()
    

    return Response({"success": True})
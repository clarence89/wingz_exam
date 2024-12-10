from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ride, RideEvent
from .serializer import RideSerializer, RideEventSerializer
from rest_framework.pagination import LimitOffsetPagination

from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return request.user and request.user.role and request.user.role.name == "admin"
        return False
    
class ViewsetPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'

@swagger_auto_schema(tags=["Rides"])
class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAdminUser]
    pagination_class = ViewsetPagination


@swagger_auto_schema(tags=["RideEvents"])
class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminUser]
    pagination_class = ViewsetPagination


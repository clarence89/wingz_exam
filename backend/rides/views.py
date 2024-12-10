from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ride, RideEvent
from .serializer import RideSerializer, RideEventSerializer
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import BasePermission
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .filters import RideFilter
import logging
logger = logging.getLogger(__name__)

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
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RideFilter
    ordering_fields = ['pickup_time'] 
    ordering = ['-pickup_time']
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset = self.filter_queryset(queryset) 
    #     print(f"Query params: {self.request.query_params}")
    #     print(f"Queryset after filters: {queryset.query}")
    #     return queryset

@swagger_auto_schema(tags=["RideEvents"])
class RideEventViewSet(viewsets.ModelViewSet):
    queryset = RideEvent.objects.all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAdminUser]
    pagination_class = ViewsetPagination

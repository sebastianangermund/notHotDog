from django.contrib.auth.models import User
from rest_framework import (
    generics,
    permissions,
    response,
    viewsets,
    decorators,
    parsers,
    status,
)

from ..photos.models import Photo
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    PhotoSerializer,
    PhotoFieldSerializer,
    FlaggedTitleSerializer,
    UserSerializer,
)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PhotoViewSet(viewsets.ModelViewSet):
    """Generic view for API methods. Handles POST and GET automatically"""
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @decorators.detail_route(
        methods=['PUT'],
        serializer_class=PhotoFieldSerializer,
        parser_classes=[parsers.MultiPartParser],
    )
    def photo(self, request, pk):
        """Handles API PUT request for the "photo" instance to model "Photo"."""
        obj = self.get_object()
        serializer = self.serializer_class(
            obj,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(
            serializer.errors,
            status.HTTP_400_BAD_REQUEST,
        )

    @decorators.detail_route(
        methods=['PUT'],
        serializer_class=FlaggedTitleSerializer,
        parser_classes=[parsers.FormParser],
    )
    def flagged(self, request, pk):
        """Handles API PUT request for instance flagged to model Photo"""
        obj = self.get_object()
        serializer = self.serializer_class(
            obj,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(
            serializer.errors,
            status.HTTP_400_BAD_REQUEST,
        )

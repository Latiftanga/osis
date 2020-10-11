from rest_framework import viewsets, mixins, generics
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from core import serializers
from core.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'staff': reverse('staff-list', request=request, format=format),
    })


class ListCreateReadUpdateViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):

    """
    A viewset that provides `retrieve`, `create`, and `list` actions.

    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset

        return queryset.filter(school=self.request.user.school)

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(
            school=self.request.user.school,
            created_by=self.request.user.email
        )

    def perform_update(self, serializer):
        serializer.save(
            updated_by=self.request.user.email
        )


class UserCreateAPIView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    # def perform_create(self, serializer):
    #     serializer.save(school=self.request.user.school)


class CreateTokenAPIView(ObtainAuthToken):
    """Create a new token for a user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CustomAuthToken(ObtainAuthToken):
    permission_classes = []
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'email': user.email
        })


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage authenticated user"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class UserCreateAPIView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer

    # def perform_create(self, serializer):
    #     serializer.save(school=self.request.user.school)


class CreateTokenAPIView(ObtainAuthToken):
    """Create a new token for a user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class CustomAuthToken(ObtainAuthToken):
    permission_classes = []
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.pk,
            'email': user.email
        })


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage authenticated user"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
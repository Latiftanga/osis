from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins, generics
from rest_framework.views import APIView
from rest_framework.settings import api_settings
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from core import serializers
from core.models import School
# from core.serializers import UserSerializer, AuthTokenSerializer, SchoolSerializer
from core.renderers import UserJSONRenderer
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
import django_filters.rest_framework
from django.contrib.auth import get_user_model

from core import serializers
from core.models import Programme, Grade


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
    # authentication_classes = (TokenAuthentication,)
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


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    # renderer_classes = (UserJSONRenderer,)
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        # user = request.data.get('user', {})
        data = {'email': request.data.get('email'), 'password': request.data.get('password')}
        print(data)
        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't  have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSets(ListCreateReadUpdateViewSet):
    authentication_classes = []
    permission_classes = []
    serializer_class = serializers.UserSerializer


class UserCreateAPIView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = serializers.UserSerializer

    # def perform_create(self, serializer):
    #     serializer.save(school=self.request.user.school)


# class CreateTokenAPIView(ObtainAuthToken):
#     """Create a new token for a user"""
#     serializer_class = AuthTokenSerializer
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# class CustomAuthToken(ObtainAuthToken):
#     permission_classes = []
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(
#             data=request.data,
#             context={'request': request}
#         )
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'id': user.pk,
#             'email': user.email
#         })


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage authenticated user"""
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class UserCreateAPIView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = serializers.UserSerializer


# class CreateTokenAPIView(ObtainAuthToken):
#     """Create a new token for a user"""
#     serializer_class = AuthTokenSerializer
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


# class CustomAuthToken(ObtainAuthToken):
#     permission_classes = []
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(
#             data=request.data,
#             context={'request': request}
#         )
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'id': user.pk,
#             'email': user.email
#         })


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage authenticated user"""
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class ProgrammeViewSets(viewsets.GenericViewSet):
    """Programme viewsets"""

    serializer_class = serializers.ProgrammeSerializer

    def get_queryset(self):
        return Programme.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GradeViewSets(ListCreateReadUpdateViewSet):
    """Grades viewsets"""
    queryset = Grade.objects.all()
    serializer_class = serializers.GradeSerializer


class SchoolViewSets(viewsets.GenericViewSet):
    """
    A simple ViewSet for viewing  school current school info.
    """
    serializer_class = serializers.SchoolSerializer

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'register_programmes':
            return serializers.RegisterProgrammes
        elif self.action == 'upload_logo':
            return serializers.SchoolLogoSerializer
        return self.serializer_class

    def get_queryset(self):
        return self.request.user.school

    def list(self, request):
        school = self.request.user.school
        serializer = self.get_serializer(school)
        return Response(serializer.data)

    @action(methods=('POST',), detail=False, url_path='register-programmes')
    def register_programmes(self, request):
        programmes = self.request.data.get('programmes', None)
        if programmes:
            school = self.request.user.school
            for programme in programmes:
                school.programmes.add(programme)
            school.save()
            return Response(data=programmes, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, url_path='upload-logo')
    def upload_logo(self, request):
        """Upload image to school instance"""
        school = self.request.user.school
        serializer = self.get_serializer(
            school,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from students import serializers
from core.serializers import UserSerializer
from core.views import ListCreateReadUpdateViewSet
from core.permissions import IsStaff
from students.models import (
    Student,
    Guardian,
)
from core.models import User


class StudentViewSet(ListCreateReadUpdateViewSet):
    """Viewset for managing student model CRUD"""

    permission_classes = (IsStaff,)
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve' or self.action == 'list' :
            return serializers.StudentDetailSerializer
        elif self.action == 'upload_image':
            return serializers.ImageUploadSerializer
        elif self.action == 'guardians' or self.action == 'guardian_list':
            return serializers.GuardianSerializer
        return self.serializer_class

    @action(methods=['post'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload image to student instance"""
        student = self.get_object()
        serializer = self.get_serializer(
            student,
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

    @action(methods=('GET', 'POST'), detail=True, url_path='guardians')
    def guardians(self, request, pk=None):
        """Create and get Guardians associated to a particular student"""

        student = self.get_object()

        if request.method == 'GET':
            guardians = student.guardians.all()
            serializer = self.get_serializer(guardians, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                guardian = serializer.save(school=self.request.user.school)
                student.guardians.add(guardian)
                student.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

    @action(methods=('GET',), detail=False, url_path='guardians')
    def guardian_list(self, request, pk=None):
        guardans = Guardian.objects.filter(school=self.request.user.school)
        serializer = self.get_serializer(guardans, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
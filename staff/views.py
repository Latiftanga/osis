from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from staff import serializers
from core.serializers import UserSerializer
from core.views import ListCreateReadUpdateViewSet
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsStaff
from staff.models import (
    Staff,
    Certificate,
    Promotion,
    Appointment
)
from core.models import User


class StaffViewSets(ListCreateReadUpdateViewSet):
    """Manage grades in the database"""
    permission_classes = (IsStaff,)
    queryset = Staff.objects.all()
    serializer_class = serializers.StaffSerializer

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve' or self.action == 'list' :
            return serializers.StaffDetailSerializer
        elif self.action == 'upload_image':
            return serializers.StaffImageSerializer
        elif self.action == 'appointment':
            return serializers.AppointmentSerializer     
        elif self.action == 'certificates' or self.action == 'certificate':
            return serializers.StaffCertificateSerializer
        elif self.action == 'promotions' or self.action == 'promotion':
            return serializers.StaffPromotionSerializer
        elif self.action == 'create_account':
            return UserSerializer
        return self.serializer_class

    @action(methods=['post'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload image to staff instance"""
        staff = self.get_object()
        serializer = self.get_serializer(
            staff,
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

    @action(methods=['GET', 'POST'], detail=True, url_path='certificates')
    def certificates(self, request, pk=None):
        staff = self.get_object()
        if self.request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    staff=staff,
                    created_by=self.request.user.email
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            certs = staff.certificates.all()
            serializer = self.get_serializer(certs, many=True)
            return Response( serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET', 'PUT', 'DELETE'], detail=True, url_path='certificates/(?P<pk1>[^/.]+)')
    def certificate(self, request, pk1=None, pk=None):
        try:
            certificate = Certificate.objects.get(pk=self.kwargs['pk1'])
        except Certificate.DoesNotExist:
            certificate = None

        if certificate and request.method == 'PUT':
            serializer = self.get_serializer(certificate, request.data)
            if serializer.is_valid():
                serializer.save(updated_by=self.request.user.email)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif certificate and request.method == 'GET':
            serializer = self.get_serializer(certificate)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        elif certificate and request.method == 'DELETE':
            certificate.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )          
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET', 'POST'], detail=True, url_path='promotions')
    def promotions(self, request, pk=None):
        staff = self.get_object()
        if self.request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    staff=staff,
                    created_by=self.request.user.email
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            promotions = staff.promotions.all()
            serializer = self.get_serializer(promotions, many=True)
            return Response( serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET', 'POST'], detail=True, url_path='certificates')
    def certificates(self, request, pk=None):
        staff = self.get_object()
        if self.request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    staff=staff,
                    created_by=self.request.user.email
                )
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        else:
            certs = staff.certificates.all()
            serializer = self.get_serializer(certs, many=True)
            return Response( serializer.data, status=status.HTTP_200_OK)

    @action(methods=['GET', 'PUT', 'DELETE'], detail=True, url_path='promotions/(?P<pk1>[^/.]+)')
    def promotion(self, request, pk1=None, pk=None):
        try:
            promotion = Promotion.objects.get(pk=self.kwargs['pk1'])
        except Promotion.DoesNotExist:
            promotion = None

        if promotion and request.method == 'PUT':
            serializer = self.get_serializer(promotion, request.data)
            if serializer.is_valid():
                serializer.save(updated_by=self.request.user.email)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif promotion and request.method == 'GET':
            serializer = self.get_serializer(promotion)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        elif promotion and request.method == 'DELETE':
            promotion.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT
            )          
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET', 'PUT', 'POST'], detail=True, url_path='appointment')
    def appointment(self, request, pk=None):
        staff = self.get_object()

        if staff.appointment and request.method == 'PUT':
            serializer = self.get_serializer(staff.appointment, request.data)
            if serializer.is_valid():
                serializer.save(updated_by=self.request.user.email)
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif staff.appointment is None and request.method == 'POST':
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                appointment = serializer.save()
                staff.appointment = appointment
                staff.save()
                return Response(
                    serializer.data,
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
        elif staff.appointment and request.method == 'POST':
            return Response(
                {'Error': f'Appointment for {staff.name} exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        elif staff.appointment and request.method == 'GET':
            serializer = self.get_serializer(staff.appointment)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        elif staff.appointment is None and request.method == 'GET':
            return Response(status=status.HTTP_204_NO_CONTENT)        
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=('POST', ), detail=True, url_path='account')
    def create_account(self, request, pk=None):
        staff = self.get_object()

        if staff.account:
            return Response(
                {'Error': f'{staff.name} already has user account'},
                status=status.HTTP_400_BAD_REQUEST               
            )
        else:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                account = serializer.save(is_teacher=True, school=self.request.user.school)
                staff.account = account
                staff.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    serializer.errors,
                    status=HTTP_400_BAD_REQUEST
                )

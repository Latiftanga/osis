from rest_framework import serializers
from staff import models
from core.models import User


class StaffCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Certificate
        fields = [
            'id',
            'category',
            'title',
            'certificate_date',
            'certificate_code',
            'certificate_description',
            'created',
            'created_by',
            'updated',
            'updated_by'
        ]
        read_only_fields = (
            'id',
            'created',
            'created_by',
            'updated',
            'updated_by'
        )


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Appointment
        fields = (
            'id',
            'category',
            'job_title',
            'job_description',
            'date_employed',
            'registered_no',
            'grade',
            'created_by',
            'updated',
            'updated_by'
        )
        read_only_fields = (
            'created',
            'created_by',
            'updated',
            'updated_by'
        )


class StaffAppointmentSerializer(serializers.ModelSerializer):

    appointment = AppointmentSerializer()

    class Meta:
        model = models.Staff
        fields = ('id', 'appointment')
        read_only_fields = ('id', )


class StaffImageSerializer(serializers.ModelSerializer):
    """Student image serializer"""

    class Meta:
        model = models.Staff
        fields = ('id', 'image')
        read_only_fields = ('id',)


class StaffCertificateSerializer(serializers.ModelSerializer):
    """Staff Certificate serializer"""

    class Meta:
        model = models.Certificate
        fields = (
            'id',
            'title',
            'category',
            'certificate_date',
            'certificate_code',
            'certificate_description',
            'created',
            'created_by',
            'updated',
            'updated_by',

        )
        read_only_fields = (
            'id',
            'created',
            'created_by',
            'updated',
            'updated_by',
        )


class StaffPromotionSerializer(serializers.ModelSerializer):
    """Staff Promotions serializers"""

    class Meta:
        model = models.Promotion
        fields = (
            'id',
            'grade',
            'date_promoted',
            'created',
            'created_by',
            'updated',
            'updated_by',
        )
        read_only_fields = (
            'id',
            'created',
            'created_by',
            'updated',
            'updated_by',
        )


class StaffPromotionDetailSerializer(StaffPromotionSerializer):
    grade = serializers.StringRelatedField(read_only=True)


class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Staff
        fields = [
            'id',
            'title',
            'first_name',
            'middle_name',
            'last_name',
            'sex',
            'date_of_birth',
            'address',
            'phone',
            'sssnit_no',
            'created',
            'created_by',
            'updated',
            'updated_by',
            'appointment',
            'certificates',
            'promotions',
            'name',
        ]
        read_only_fields = (
            'id',
            'name',
            'appointment',
            'promotions',
            'certificates',
            'created',
            'created_by',
            'updated',
            'updated_by'
        )


class StaffDetailSerializer(StaffSerializer):
    appointment = AppointmentSerializer(read_only=True)
    certificates = StaffCertificateSerializer(read_only=True, many=True)
    promotions = StaffPromotionDetailSerializer(read_only=True, many=True)

from rest_framework import serializers
from students.models import (
    Student,
    Guardian
)


class StudentSerializer(serializers.ModelSerializer):
    """Student model serializer"""

    class Meta:
        model = Student
        fields = (
            'id',
            'index_no',
            'first_name',
            'middle_name',
            'last_name',
            'sex',
            'date_of_birth',
            'place_of_birth',
            'hometown',
            'home_address',
            'mobile_phone',
            'email',
            'guardians',
            'image',
            'created',
            'created_by',
            'updated',
            'updated_by'
        )
        read_only_fields = (
            'id',
            'guardians',
            'image',
            'created',
            'created_by',
            'updated',
            'updated_by',
        )


class ImageUploadSerializer(serializers.ModelSerializer):
    """Serializer that upload students image"""

    class Meta:
        model = Student
        fields = ('id', 'image')
        read_only_fields = ('id', )


class GuardianSerializer(serializers.ModelSerializer):
    """Guardian model serializer"""

    class Meta:
        model = Guardian
        fields = (
            'id',
            'title',
            'name',
            'sex',
            'occupation',
            'office_phone',
            'mobile_phone',
            'email',
            'address',
            'postal_code',
            'relation_to_student',
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


class StudentDetailSerializer(StudentSerializer):
    """Student Detail serializer for client view"""

    guardians = GuardianSerializer(many=True)

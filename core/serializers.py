from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from core.models import Programme, Grade, School

class UserSerializer(serializers.ModelSerializer):
    """Serializer for converting user model object"""

    class Meta():
        model = get_user_model()
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password', 'trim_whitespace': False}
    )

    def validate(self, attrs):
        """Validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')
        attrs['user'] = user
        return attrs

class ProgrammeSerializer(serializers.ModelSerializer):
    """Programme serializer"""

    class Meta:
        model = Programme
        fields = (
            'id',
            'name',
            'code',
        )
        read_only_fields = (
            'id',
        )


class RegisterProgrammes(serializers.ModelSerializer):

    programmes = serializers.PrimaryKeyRelatedField(
        read_only=False,
        many=True,
        queryset=Programme.objects.all()
    )

    class Meta:
        model = School
        fields = ('id', 'programmes')
        read_only_fields = ('id',)


class GradeSerializer(serializers.ModelSerializer):
    """Programme serializer"""

    class Meta:
        model = Grade
        fields = (
            'id',
            'name',
            'year',
            'programme',
            'created',
            'created_by',
            'updated',
            'updated_by'
        )
        read_only_fields = (
            'id',
            'created',
            'created_by',
            'updated',
            'updated_by'
        )


class SchoolSerializer(serializers.ModelSerializer):

    programmes = serializers.StringRelatedField(many=True)
    class Meta:
        model = School
        fields = (
            'id',
            'name',
            'level',
            'code',
            'motto',
            'logo',
            'address',
            'city',
            'region',
            'phone',
            'postal_code',
            'email',
            'programmes',
        )
        read_only_fields = (
            'id',
        )


class SchoolLogoSerializer(serializers.ModelSerializer):
    """Serializer that upload logo to school instance"""

    class Meta:
        model = School
        fields = ('id', 'logo')
        read_only_fields = ('id', )
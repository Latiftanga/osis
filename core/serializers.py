from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from core.models import Programme, Grade, School


class UserSerializer(serializers.ModelSerializer):
    """Serializer for converting user model object"""

    # token = serializers.SerializerMethodField()
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta():
        model = get_user_model()
        fields = ('token', 'email', 'password')
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

    # def get_token(self, obj):
    #     jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    #     jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    #     payload = jwt_payload_handler(obj)
    #     token = jwt_encode_handler(payload)
    #     return token


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # our database.
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. Notice how
        # we pass `email` as the `username` value since in our User
        # model we set `USERNAME_FIELD` as `email`.
        user = authenticate(email=email, password=password)

        # If no user was found matching this email/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`. The
        # purpose of this flag is to tell us whether the user has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'email': user.email,
            'token': user.token
        }


class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email',)


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for user authentication object"""
    email = serializers.EmailField()
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

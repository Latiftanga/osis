import os
from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
import jwt


def school_logo_file_path(instance, filename):
    """Generate file path for new school logo"""
    ext = filename.split('.')[-1]  # [-1] returns the last item from a list
    filename = f'{instance.name}_{instance.id}.{ext}'

    return os.path.join('uploads/schools/', filename)


class UserManager(BaseUserManager):
    """ """

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a new user """

        if not email:
            raise ValueError('Users must have a valid email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and save a new super user"""
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_staff(self, email, password):
        """Create and save a new staff(admin) user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_teacher(self, email, password):
        """Create and save a new teacher user"""
        user = self.create_user(email, password)
        user.is_teacher = True
        user.save(using=self._db)
        return user

    def create_student(self, email, password):
        """Create and save a new student user"""
        user = self.create_user(email, password)
        user.is_student = True
        user.save(using=self._db)
        return user

    def create_parent(self, email, password):
        """Create and save a new parent user"""
        user = self.create_user(email, password)
        user.is_parent = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    school = models.ForeignKey(
        'School',
        on_delete=models.CASCADE,
        related_name='users',
        blank=True,
        null=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    is_parent = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    # @property
    # def token(self):
    #     """
    #     Allows us to get a user's token by calling `user.token` instead of
    #     `user.generate_jwt_token().

    #     The `@property` decorator above makes this possible. `token` is called
    #     a "dynamic property".
    #     """
    #     return self._generate_jwt_token()

    # def _generate_jwt_token(self):
    #     """
    #     Generates a JSON Web Token that stores this user's ID and has an expiry
    #     date set to 60 days into the future.
    #     """
    #     dt = datetime.now() + timedelta(days=60)

    #     token = jwt.encode({
    #         'id': self.pk,
    #         'exp': int(dt.strftime('%s'))
    #     }, settings.SECRET_KEY, algorithm='HS256')

    #     return token.decode('utf-8')


class School(models.Model):
    """School object"""
    SCHOOL_LEVELS = (
        ('PRIMARY', 'Primary'),
        ('JHS', 'Junior High'),
        ('SHS', 'Senior High'),
        ('TERTIARY', 'Tertiary')
    )
    name = models.CharField(max_length=64, unique=True)
    level = models.CharField(max_length=8, choices=SCHOOL_LEVELS)
    motto = models.CharField(max_length=255, blank=True)
    code = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=64)
    region = models.CharField(max_length=32)
    phone = models.CharField(max_length=20, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=64, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)
    logo = models.ImageField(
        blank=True,
        null=True,
        upload_to=school_logo_file_path
    )
    programmes = models.ManyToManyField(
        'Programme',
        related_name='schools'
    )

    def __str__(self):
        return self.name


class Programme(models.Model):
    """Student programmes"""

    name = models.CharField(max_length=32, unique=True)
    code = models.CharField(max_length=16, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f'{self.name}'


class Grade(models.Model):
    """Grade model """

    YEARS_IN_SCHOOL = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6)
    )
    name = models.CharField(max_length=32, unique=True)
    year = models.PositiveSmallIntegerField(unique=True, choices=YEARS_IN_SCHOOL)
    programme = models.ForeignKey(
        Programme,
        related_name='grades',
        on_delete=models.CASCADE
    )
    school = models.ForeignKey(
        School,
        related_name='grades',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f'{self.year}{self.name}'

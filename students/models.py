import os
from django.db import models
from core.models import School, User, Grade


def student_image_file_path(instance, filename):
    """Generate file path for new school logo"""
    ext = filename.split('.')[-1]  # [-1] returns the last item from a list
    filename = f'{instance.index_no}.{ext}'

    return os.path.join('uploads/students/', filename)


class Guardian(models.Model):
    """Student guardian object"""

    SEX_CHOICES = (('M', 'Male'), ('F', 'Female'))

    title = models.CharField(max_length=16, blank=True)
    name = models.CharField(max_length=128)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    occupation = models.CharField(max_length=64)
    office_phone = models.CharField(max_length=20, blank=True)
    mobile_phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=64, blank=True)
    address = models.CharField(max_length=128)
    postal_code = models.CharField(max_length=16, blank=True)
    relation_to_student = models.CharField(max_length=32)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='guardians'
    )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f'{self.title} {self.name}'


class Student(models.Model):
    """Student model object"""

    SEX_CHOICES = (('M', 'Male'), ('F', 'Female'))

    index_no = models.CharField(max_length=128, unique=True)
    first_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=64, blank=True)
    hometown = models.CharField(max_length=64, blank=True)
    home_address = models.CharField(max_length=128, blank=True)
    mobile_phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=64, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)
    grade = models.ForeignKey(
        Grade,
        on_delete=models.CASCADE,
        related_name='students',
        null=True,
        blank=True
    )
    account = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        blank=True,
        null=True
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to=student_image_file_path
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='students'
    )
    guardians = models.ManyToManyField(
        Guardian,
        related_name='students',
    )
    @property
    def name(self):
        return f'{self.last_name} {self.middle_name} {self.first_name}'

    def __str__(self):
        return self.name

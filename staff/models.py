import uuid
import os

from django.db import models
from core.models import School, User


def staff_image_file_path(instance, filename):
    """Generate file path for new school logo"""
    ext = filename.split('.')[-1]  # [-1] returns the last item from a list
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join('uploads/staff/', filename)

class Staff(models.Model):
    SEX_CHOICES = (('M', 'Male'), ('F', 'Female'))
    TITLES = (
        ('Mr', 'Mr'),
        ('Ms', 'Ms'),
        ('Mrs', 'Mrs'),
        ('Dr', ('Dr')),
        ('Prof', 'Prof'),
        ('Rev', 'Rev'),
        ('Maulvi', 'Maulvi'),
    )
    title = models.CharField(max_length=32, blank=True, choices=TITLES)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    sssnit_no = models.CharField(max_length=32, blank=True)
    appointment = models.OneToOneField(
        'Appointment',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='staff'
    )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)
    account = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='staff_profile',
        blank=True,
        null=True
    )
    image = models.ImageField(
        blank=True,
        null=True,
        upload_to=staff_image_file_path
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='staff'
    )
    @property
    def name(self):
        return f'{self.title} {self.last_name} {self.middle_name} {self.first_name}'

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'staff'
        verbose_name_plural = 'staff'
        ordering = ['last_name']


class Certificate(models.Model):
    """Staff Qualifications"""
    CERT_CATEGORIES = (
        ('Academic', 'Academic'),
        ('Professional', 'Professional'),
        ('Hybrid', 'Hybrid')
    )
    category = models.CharField(max_length=16, choices=CERT_CATEGORIES)
    title = models.CharField(max_length=255)
    certificate_date =models.DateField()
    certificate_code = models.CharField(max_length=8, blank=True)
    certificate_description = models.CharField(max_length=255, blank=True)
    staff = models.ForeignKey(
        Staff,
        on_delete=models.CASCADE,
        related_name='certificates'
    )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)


    def __str__(self):
        return f'{self.title} {self.certificate_date}'


class Appointment(models.Model):
    """Staff employment info"""
    STAFF_CATEGORIES = (
        (1, 'Teaching'),
        (2, 'Non Teaching')
    )
    category = models.PositiveIntegerField(choices=STAFF_CATEGORIES)
    job_title = models.CharField(max_length=64)
    job_description = models.CharField(max_length=255, blank=True)
    date_employed = models.DateField()
    staff_id = models.CharField(max_length=16, blank=True)
    registered_no = models.CharField(max_length=16, blank=True)
    grade = models.ForeignKey(
        'Grade',
        null=True,
        on_delete=models.CASCADE,
        blank=True,
        related_name='appointment'
    )
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f'{self.date_employed}'


class Grade(models.Model):
    name = models.CharField(max_length=128)
    promotions = models.ManyToManyField(Staff, through='Promotion')
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']


class Promotion(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='promotions')
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    date_promoted = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=64, blank=True)
    updated = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f'{self.grade.name}, {self.date_promoted}'

    class Meta:
        ordering = ['-date_promoted']

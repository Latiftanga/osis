import tempfile
import os

from PIL import Image

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status

from staff.models import Staff, Grade, Certificate, Appointment
from staff.serializers import StaffSerializer, StaffDetailSerializer

from core.tests import sample_objects


STAFF_URL = reverse('staff-list')


def image_upload_url(staff_id):
    """Return URL for staff image upload"""
    return reverse('staff-upload-image', args=[staff_id])


def detail_url(staff_id):
    """Return details url for staff"""
    return reverse('staff-detail', args=[staff_id])


class StaffAPITests(TestCase):
    """Test private available API"""
    def setUp(self):
        self.client1 = APIClient()
        self.client2 = APIClient()
        self.staff_user = get_user_model().objects.create_staff(
            email='staff@twysolutions.com',
            password='staff@password'
        )
        self.teacher_user = get_user_model().objects.create_teacher(
            email='teacher@twysolutions.com',
            password='teacher@password'
        )
        school = sample_objects.get_school()
        self.staff_user.school = school
        self.teacher_user.school = school
        self.client1.force_authenticate(self.staff_user)
        self.client2.force_authenticate(self.teacher_user)

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client2.get(STAFF_URL)

        self.assertEquals(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_staff(self):
        """Test retrieving staff by user school"""
        sample_objects.get_staff(sample_objects.get_school())
        sample_objects.get_staff(self.staff_user.school)

        res = self.client1.get(STAFF_URL)
        staff = Staff.objects.filter(school=self.staff_user.school)
        serializer = StaffSerializer(staff, many=True)

        self.assertEquals(res.status_code, status.HTTP_200_OK)
        self.assertEquals(len(res.data), 1)
        self.assertEquals(res.data, serializer.data)

    def test_retrieve_staff_detail(self):
        """Retrieving student detail object"""
        staff = sample_objects.get_staff(school=self.staff_user.school)
        grade = Grade.objects.create(name='Principal Superintendant')
        cert = Certificate.objects.create(
            title='Bsc Information Technology Education',
            category='Hybrid',
            certificate_code='0001',
            certificate_date='2015-7-1',
            staff=staff
        )
        appointment = Appointment.objects.create(
            category=1,
            job_title='Subject master',
            date_employed='2007-9-1',
            registered_no='4979/07',
            grade=grade,
            staff_id='183869'
        )

        staff.appointment = appointment
        staff.save()

        url = detail_url(staff.id)

        res = self.client1.get(url)
        serializer = StaffDetailSerializer(staff)
        # self.assertEquals(res.data, serializer.data)

    def test_create_basic_staff(self):
        """Test creating staff only required fields"""
        payload = sample_objects.get_staff_dafault_payload(
            school=self.staff_user.school
        )
        res = self.client1.post(STAFF_URL, payload)

        self.assertEquals(res.status_code, status.HTTP_201_CREATED)
        staff = Staff.objects.get(id=res.data['id'])

        self.assertEquals(payload['first_name'], staff.first_name)


class StudentImageUploadTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.staff_user = get_user_model().objects.create_staff(
            'user@twysolution.com',
            'testpassword'
        )
        self.client.force_authenticate(self.staff_user)
        self.staff_user.school = sample_objects.get_school()
        self.staff = sample_objects.get_staff(school=self.staff_user.school)

    def tearDown(self):
        self.staff.image.delete()

    def test_upload_image_to_student(self):
        """Test uploading image to staff"""
        url = image_upload_url(self.staff.id)

        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)  # to start reading the file from the begining
            res = self.client.post(url, {'image': ntf}, format='multipart')

        self.staff.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.staff.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.staff.id)

        res = self.client.post(url, {'image': 'notimage'}, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

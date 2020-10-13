from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from staff.views import StaffViewSets
from students.views import StudentViewSet
from core.views import ProgrammeViewSets, SchoolViewSets, GradeViewSets

router = routers.DefaultRouter()
router.register('school', SchoolViewSets, basename='school')
router.register('staff', StaffViewSets)
router.register('programmes',ProgrammeViewSets, basename='programmes')
router.register('grades',GradeViewSets, basename='grades')
router.register('students', StudentViewSet, basename='students')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('core.urls')),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

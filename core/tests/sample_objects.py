from core.models import School, User
from staff.models import Staff
from core.tests.faker import fake


def get_school(**params):
    """Create a sample schol and return it"""
    defaults = {
        'name': fake.name().split(' ')[0],
        'level': fake.school_levels(),
        'motto': fake.name(),
        'code': fake.date(),
        'address': fake.address(),
        'city': fake.city(),
        'region': fake.region(),
        'email': fake.email(),
    }
    defaults.update(params)  # Overwrite or add addtional key/values

    return School.objects.create(**defaults)


def get_get_staff_user(**params):
    """Create a sample schol and return it"""
    defaults = {
        'email': fake.email(),
        'password': 'staff@password',
    }
    defaults.update(params)  # Overwrite or add addtional key/values

    return User.objects.create_staff(**defaults)


def get_get_teacher_user(**params):
    """Create a sample schol and return it"""
    defaults = {
        'email': fake.email(),
        'password': 'teacher@password',
    }
    defaults.update(params)

    return User.objects.create_teacher(**defaults)


def get_get_student_user(**params):
    """Create a sample schol and return it"""
    defaults = {
        'email': fake.email(),
        'password': 'student@password',
    }
    defaults.update(params)

    return User.objects.create_student(**defaults)


def get_get_parent_user(**params):
    """Create a sample schol and return it"""
    defaults = {
        'email': fake.email(),
        'password': 'staff@password',
        'is_parent': True,
    }
    defaults.update(params)

    return User.objects.create_parent(**defaults)


def get_staff(school, **params):
    """Create a sample staff and return it"""
    defaults = {
        'first_name': fake.name().split(' ')[0],
        'last_name': fake.name().split(' ')[-1],
        'sex': fake.sex(),
        'date_of_birth': fake.date(),
        'address': fake.address(),
        'email': fake.email()
    }
    defaults.update(params)  # Overwrite or add addtional key/values

    return Staff.objects.create(school=school, **defaults)


def get_staff_dafault_payload(**params):
    """Return sample staff payload for only required fields"""
    name = fake.name()
    defaults = {
        'first_name': name.split(' ')[0],
        'last_name': name.split(' ')[1],
        'sex': fake.sex(),
        'date_of_birth': fake.date(),
        'address': fake.address(),
        'email': fake.email()
    }
    defaults.update(params)
    return defaults
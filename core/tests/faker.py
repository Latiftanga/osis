import random
from faker import Faker
from faker.providers import BaseProvider

fake = Faker()


class CoreProvider(BaseProvider):
    def region(self):
        regions = [
            'UW', 'UE', 'NR', 'BR', 'BE', 'AHAFO',
            'AR', 'ER', 'WR', 'GR', 'SR', 'OTI', 'VR',
            'CR', 'NER', 'WNR'
        ]
        return random.choice(regions)

    def city(self):
        cities = [
            'Wa', 'Nadowli', 'Kaleo',
            'Jirapa', '', 'Tumu', 'Gwollu',
            'Hamile', 'Sombo', 'Babile'
        ]
        return random.choice(cities)

    def school_levels(self):
        levels = ['PRIMARY', 'JHS', 'SHS', 'TERTIARY']
        return random.choice(levels)

    def guardian_relation(self):
        relations = [
            'Father', 'Mother', 'Brother', 'Sister',
            'Uncle', 'Aunt', 'Grandfather', 'Grandmother'
        ]
        return random.choice(relations)

    def sex(self):
        sexes = ['M', 'F']
        return random.choice(sexes)

    def student_status(self):
        statuses = ['Boarding', 'Day']
        return random.choice(statuses)

    def year(self):
        years = [1, 2, 3]
        return random.choice(years)

    def programme_division(self):
        divisions = [
            'A', 'B', 'C', 'D', 'E',
            'F', 'G', 'H', 'I', 'J', 'K'
        ]
        return random.choice(divisions)

    def programme(self):
        programmes = [
            'Agricultural Science',
            'Business',
            'General Arts',
            'General Science',
            'Home Economics',
            'Visual Arts'
        ]
        return random.choice(programmes)



fake.add_provider(CoreProvider)

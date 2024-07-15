# restaurant/management/commands/populate_timeslots.py
from django.core.management.base import BaseCommand
from restaurant.models import Timeslot

class Command(BaseCommand):
    help = 'Populates the database with predefined timeslots'

    def handle(self, *args, **options):
        Timeslot.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all existing timeslots.'))

        timeslots = [
            ("10:00 AM", "11:30 AM"),
            ("10:30 AM", "12:00 PM"),
            ("11:00 AM", "12:30 PM"),
            ("11:30 AM", "01:00 PM"),
            ("12:00 PM", "01:30 PM"),
            ("12:30 PM", "02:00 PM"),
            ("01:00 PM", "02:30 PM"),
            ("01:30 PM", "03:00 PM"),
            ("02:00 PM", "03:30 PM"),
            ("02:30 PM", "04:00 PM"),
            ("03:00 PM", "04:30 PM"),
            ("03:30 PM", "05:00 PM"),
            ("04:00 PM", "05:30 PM"),
            ("04:30 PM", "06:00 PM"),
            ("05:00 PM", "06:30 PM"),
            ("05:30 PM", "07:00 PM"),
            ("06:00 PM", "07:30 PM"),
            ("06:30 PM", "08:00 PM"),
            ("07:00 PM", "08:30 PM"),
            ("07:30 PM", "09:00 PM"),
            ("08:00 PM", "09:30 PM"),
        ]

        for start, end in timeslots:
            if not Timeslot.objects.filter(start_time=start, end_time=end).exists():
                Timeslot.objects.create(start_time=start, end_time=end)
                self.stdout.write(self.style.SUCCESS(f'Successfully added timeslot {start} - {end}'))
            else:
                self.stdout.write(f'Timeslot {start} - {end} already exists.')
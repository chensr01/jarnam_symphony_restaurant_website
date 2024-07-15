# your_app/management/commands/populate_tables.py
from django.core.management.base import BaseCommand
from restaurant.models import Table

class Command(BaseCommand):
    help = 'Populates the database with predefined tables'

    def handle(self, *args, **kwargs):
        Table.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully cleared all existing tables.'))

        # Define table data
        table_data = [
            {'table_name': 'two-table-1', 'capacity': 2},
            {'table_name': 'two-table-2', 'capacity': 2},
            {'table_name': 'two-table-3', 'capacity': 2},
            {'table_name': 'two-table-4', 'capacity': 2},
            {'table_name': 'two-table-5', 'capacity': 2},
            {'table_name': 'two-table-6', 'capacity': 2},
            {'table_name': 'two-table-7', 'capacity': 2},
            {'table_name': 'two-table-8', 'capacity': 2},
            {'table_name': 'four-table-1', 'capacity': 4},
            {'table_name': 'four-table-2', 'capacity': 4},
            {'table_name': 'four-table-3', 'capacity': 4},
            {'table_name': 'four-table-4', 'capacity': 4},
            {'table_name': 'six-table-1', 'capacity': 6},
            {'table_name': 'six-table-2', 'capacity': 6},
        ]

        # Create each table if it doesn't already exist
        for table_info in table_data:
            table_name = table_info['table_name']
            capacity = table_info['capacity']

            # Check if the table already exists
            if not Table.objects.filter(table_name=table_name).exists():
                Table.objects.create(table_name=table_name, capacity=capacity)
                self.stdout.write(self.style.SUCCESS(f'Successfully created {table_name} with capacity {capacity}'))
            else:
                self.stdout.write(self.style.WARNING(f'{table_name} already exists. No changes made.'))

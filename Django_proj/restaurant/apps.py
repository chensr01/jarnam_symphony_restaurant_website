from django.apps import AppConfig


class RestaurantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'restaurant'

    def ready(self):
        pass
        # from django.core.management import call_command
        # call_command('populate_timeslots')
        # call_command('populate_tables')
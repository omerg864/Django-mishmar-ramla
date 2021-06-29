from django.apps import AppConfig


class ScheduleConfig(AppConfig):
    name = 'Schedule'

    def ready(self):
        import Schedule.signals

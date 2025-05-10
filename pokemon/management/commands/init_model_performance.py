from django.core.management.base import BaseCommand
from pokemon.models import ModelPerformance

class Command(BaseCommand):
    help = 'Initialize model performance data'

    def handle(self, *args, **kwargs):
        # Initial accuracy values - you can adjust these based on your actual model performance
        model_data = [
            ('best', 87.5),
            ('svc', 85.2),
            ('dtc', 82.1),
            ('rfc', 86.3),
        ]

        for model_name, accuracy in model_data:
            ModelPerformance.objects.create(
                model_name=model_name,
                accuracy=accuracy
            )
            self.stdout.write(
                self.style.SUCCESS(f'Successfully created {model_name} performance data')
            )
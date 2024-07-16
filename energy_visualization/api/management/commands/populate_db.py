import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from api.models import User, EnergyData

class Command(BaseCommand):
    help = 'Populate the EnergyData table from energyData.csv'

    def handle(self, *args, **kwargs):
        # Get the directory where manage.py is located
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        # Construct the full path to the energyData.csv file
        csv_file_path = os.path.join(base_dir, 'energyData.csv')
        
        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                username = row['username']
                user, created = User.objects.get_or_create(username=username, defaults={'email': f'{username}@example.com', 'password': 'password'})
                EnergyData.objects.create(
                    username=user,
                    energy_source=row['energy_source'],
                    consumption=row['consumption'],
                    generation=row['generation'],
                    timestamp=datetime.strptime(row['timestamp'], "%Y-%m-%dT%H:%M:%S")
                )
        self.stdout.write(self.style.SUCCESS('Successfully populated EnergyData table'))

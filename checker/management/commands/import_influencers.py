from django.core.management.base import BaseCommand
from checker.utils.influencers_import import import_influencers_and_follows_from_csv

class Command(BaseCommand):
    help = "Import influencers and their followings from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument('csv_path', type=str, help='Path to the CSV file with influencers')

    def handle(self, *args, **kwargs):
        csv_path = kwargs['csv_path']
        self.stdout.write(f"Importing from {csv_path}...")
        import_influencers_and_follows_from_csv(csv_path)
        self.stdout.write(self.style.SUCCESS("Import completed."))

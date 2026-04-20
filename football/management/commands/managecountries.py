from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from football.models import Country
# from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = "Perform Country commands"
    count = 0

    def add_arguments(self, parser):
        parser.add_argument(
            "-a",
            "--action",
            choices=["retrieve", "list"],
            required=True,
            help="Action to take"
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS(f"Processing complete:{options['action']}"))

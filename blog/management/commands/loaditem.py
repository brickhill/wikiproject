from django.core.management.base import BaseCommand
from blog.transport import loadit

class Command(BaseCommand):
    help = "Load an item"

    def add_arguments(self, parser):
        parser.add_argument(
            "--slug",
            required=False,
            type=str,
        )
        parser.add_argument(
            "--type",
            required=True,
            help="page/post",
            choices=['page', 'post']
        )

    def handle(self, *args, **options):
        # Command logic

        self.stdout.write(
            self.style.SUCCESS("Command started"))
        self.stdout.write(
            self.style.SUCCESS(f"option:{options['slug']}")
        )

        loadit(self, slug=options['slug'], type=options['type'])
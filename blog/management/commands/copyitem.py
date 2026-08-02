from django.core.management.base import BaseCommand
from blog.transport import dumpit

class Command(BaseCommand):
    help = "Description of what this command does"

    def add_arguments(self, parser):
        parser.add_argument(
            "--slug",
            required=False,
            type=str,        # type=int
        )
        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Overwrite existing data?",
        )
        parser.add_argument(
            "--type",
            required=True,
            help="page/post",
            choices=['page', 'post']
        )

    def handle(self, *args, **options):
        # Command logic
        for o1 in options:
            self.stdout.write(
                self.style.SUCCESS(f"{o1}:{options[o1]}")
            )
        self.stdout.write(
            self.style.SUCCESS("Command started"))
        self.stdout.write(
            self.style.SUCCESS(f"option:{options['slug']}")
        )
        if options['overwrite']:
            self.stdout.write(
                self.style.ERROR("OVERWRITE"))

        dumpit(self, slug=options['slug'], type=options['type'])
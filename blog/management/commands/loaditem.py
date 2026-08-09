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
        parser.add_argument(
            "--all",
            action="store_true",
            help="Load all items"
        )

    def handle(self, *args, **options):
        # Command logic

        self.stdout.write(
            self.style.SUCCESS("Command started"))
        self.stdout.write(
            self.style.SUCCESS(f"option:{options['slug']}:ALL{options['all']}")
        )
        if options["slug"] is not None and options["all"] is True:
            self.stdout.write(
                self.style.ERROR("Don't specify slug and __all"))
            exit()
        if options["slug"] is None and options["all"] is False:
            self.stdout.write(
                self.style.ERROR("Specify slug or __all")
            )
            exit()
        loadit(self, slug=options['slug'], type=options['type'], all=options["all"])
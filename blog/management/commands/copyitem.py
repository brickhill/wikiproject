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

        parser.add_argument(
            "--all",
            action="store_true",
            help="Dump all items"
        )

    def handle(self, *args, **options):
        # Command logic
        if options["slug"] is not None and options["all"] is True:
            self.stdout.write(
                self.style.ERROR("Don't specify slug and __all"))
            exit()
        if options["slug"] is None and options["all"] is False:
            self.stdout.write(
                self.style.ERROR("Specify slug or __all")
            )
            exit()
        
        # for o1 in options:
        #     self.stdout.write(
        #         self.style.SUCCESS(f"{o1}:{options[o1]}")
        #     )
        self.stdout.write(
            self.style.SUCCESS("Command started"))
        self.stdout.write(
            self.style.SUCCESS(f"option:{options['slug']}")
        )
        if options['overwrite']:
            self.stdout.write(
                self.style.ERROR("OVERWRITE"))
        dumpit(self, slug=options['slug'], all=options["all"], type=options['type'])

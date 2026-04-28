from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from football.models import Country
from football.sparql import WikidataQueryBuilder
import requests
import pickle
# from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = "Perform Country commands"
    count = 0

    def add_arguments(self, parser):
        parser.add_argument(
            "-a",
            "--action",
            choices=["retrieve", "list", "pickle", "process"],
            required=True,
            help="Action to take"
        )
        parser.add_argument(
           "-f",
           "--filename",
           required=False,
           help="Filename for storing temporary data"
        )

    def handle(self, *args, **options):
        action = options["action"]
        filename = options["filename"]
        if action == "pickle" and not filename:
            raise CommandError("--filename is required when --action=pickle")

        if action == "pickle" or action == "process":
            builder = WikidataQueryBuilder()

            # query = (
            #         builder
            #         .only_humans()
            #         .with_sport("Q937857")   # footballer
            #         .with_country("Q145")    # United Kingdom
            #         .with_image(required=False)
            #         .set_limit(100)
            #         .build()
            #         )
            query = (
                builder.only_countries().build()
            )
            print(query)
            data = self.run_query(query)
            results = self.parse_results(data)
            print(results)
            if action == "pickle":
                with open(filename, "wb") as f:
                    pickle.dump(results, f)
            self.stdout.write(self.style.SUCCESS(results))
        self.stdout.write(self.style.SUCCESS(f"Processing complete:{options['action']}"))

    def run_query(self, query):
        url = "https://query.wikidata.org/sparql"

        headers = {
            "Accept": "application/json",
            "User-Agent": "PGDjangoApp/1.0 (petergibson@sbsys.co.uk)"
        }

        r = requests.get(url, params={"query": query}, headers=headers)
        r.raise_for_status()
        return r.json()

    def parse_results(self, data):
        results = []

        for row in data["results"]["bindings"]:
            results.append({
                "id": row["country"]["value"].split("/")[-1],
                "name": row["countryLabel"]["value"]
            })

        return results
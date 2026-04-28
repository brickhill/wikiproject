import textwrap

class WikidataQueryBuilder:
    BASE_PREFIX = """
    SELECT ?country ?countryLabel WHERE {
    """

    FOOTER = """
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    """

    def __init__(self):
        self.filters = []
        self.limit = 500
        self.require_image = False

    def with_sport(self, sport_qid):
        # occupation (P106)
        self.filters.append(f"?person wdt:P106 wd:{sport_qid} .")
        return self
    
    def only_countries(self):
        # Instance of Country.
        self.filters.append("?country wdt:P31 wd:Q6256 .")
        return self

    def with_country(self, country_qid):
        # country of citizenship (P27)
        self.filters.append(f"?person wdt:P27 wd:{country_qid} .")
        return self

    def only_humans(self):
        # instance of human (Q5)
        self.filters.append("?person wdt:P31 wd:Q5 .")
        return self

    def with_image(self, required=False):
        self.require_image = required
        if required:
            self.filters.append("?person wdt:P18 ?image .")
        else:
            self.filters.append("OPTIONAL { ?person wdt:P18 ?image . }")
        return self

    def set_limit(self, limit):
        self.limit = limit
        return self

    def build(self):
        where_block = "\n  ".join(self.filters)

        query = f"""
        {self.BASE_PREFIX}
          {where_block}
        {self.FOOTER}
        LIMIT {self.limit}
        """

        return textwrap.dedent(query).strip()
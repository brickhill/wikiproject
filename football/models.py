from django.db import models
# from django.contrib.auth.models import User


class Country(models.Model):
    name = models.CharField(max_length=30,
                            db_index=True,
                            unique=True,
                            null=False,
                            blank=False,
                            help_text="Country")

    def clean(self):
        self.name = self.name.title()

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

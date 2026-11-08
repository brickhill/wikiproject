from django.contrib.auth.models import User
from django.db import models


class Organisation(models.Model):
    name = models.CharField(max_length=200)
    created_by = models.ForeignKey(
                                   User,
                                   on_delete=models.PROTECT,
                                   related_name="owned_organisations"
    )


    class Meta:
        unique_together = ["name", "created_by"]


class Membership(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("author", "Author"),
        ("viewer", "Viewer"),
    ]
    organisation = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    class Meta:
        unique_together = ["organisation", "user"]

from django.db import models
import uuid


from main import settings


class Poll(models.Model):
    PUBLIC = "public"
    PRIVATE = "private"
    SEMI = "semi"

    POLL_TYPE_CHOICES = [
        (PUBLIC, "Public (anyone can vote)"),
        (PRIVATE, "Private (only invited users)"),
        (SEMI, "Semi-public (authenticated users)"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    creator_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_closed = models.BooleanField(default=False)
    selected_slot = models.ForeignKey(
        "Slot", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    poll_type = models.CharField(
        max_length=10, choices=POLL_TYPE_CHOICES, default=PUBLIC
    )
    invited_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True
    )  # for private polls

    def __str__(self):
        return self.title


class Slot(models.Model):
    poll = models.ForeignKey(Poll, related_name="slots", on_delete=models.CASCADE)
    datetime = models.DateTimeField()

    class Meta:
        ordering = ["datetime"]

    def __str__(self):
        return f"{self.poll.title} - {self.datetime}"


class Vote(models.Model):
    slot = models.ForeignKey(Slot, related_name="votes", on_delete=models.CASCADE)
    voter_name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("slot", "voter_name")

    def __str__(self):
        return f"{self.voter_name} - {self.slot.datetime}"

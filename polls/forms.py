from django import forms
from django.forms import inlineformset_factory
from .models import Poll, Slot

from django import forms
from django.contrib.auth import get_user_model
from .models import Poll
from main import settings

from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Poll

User = get_user_model()


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ["title", "description", "creator_name", "poll_type", "invited_users"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "description": forms.Textarea(
                attrs={"class": "textarea textarea-bordered w-full"}
            ),
            "creator_name": forms.TextInput(
                attrs={"class": "input input-bordered w-full"}
            ),
            "poll_type": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "invited_users": forms.SelectMultiple(
                attrs={"class": "select select-bordered w-full"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        UserModel = settings.AUTH_USER_MODEL
        self.fields["invited_users"].queryset = User.objects.filter(
            is_staff=False, is_superuser=False
        )


SlotFormSet = inlineformset_factory(
    Poll,
    Slot,
    fields=["datetime"],
    extra=3,
    widgets={
        "datetime": forms.DateTimeInput(
            attrs={"type": "datetime-local", "class": "input input-bordered w-full"}
        ),
    },
)

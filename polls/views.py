from django.views.generic import CreateView, ListView, DetailView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import Poll, Slot, Vote
from .forms import PollForm, SlotFormSet
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Poll, Slot

from django.http import HttpResponse
from ics import Calendar, Event
from .functions import Validate
from django.db.models import Count, Max

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


class CreateView(CreateView):
    model = Poll
    form_class = PollForm
    template_name = "polls/create_poll.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = SlotFormSet(self.request.POST)
        else:
            context["formset"] = SlotFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        if formset.is_valid():
            response = super().form_valid(form)
            slots = formset.save(commit=False)
            for slot in slots:
                slot.poll = self.object
                slot.save()

            user_polls = self.request.session.get("user_polls", [])
            user_polls.append(str(self.object.id))
            self.request.session["user_polls"] = user_polls

            return response
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse_lazy("polls:details", kwargs={"poll_id": self.object.id})


class UserListView(ListView):
    model = Poll
    template_name = "polls/poll_list.html"
    context_object_name = "polls"

    def get_queryset(self):
        user_polls = self.request.session.get("user_polls", [])
        polls = (
            Poll.objects.filter(id__in=user_polls)
            .annotate(total_votes=Count("slots__votes"))
            .order_by("-created_at")
        )

        for poll in polls:
            poll.top_slot = (
                poll.slots.annotate(vote_count=Count("votes"))
                .order_by("-vote_count", "datetime")
                .first()
            )
            poll.full_url = self.request.build_absolute_uri(
                reverse("polls:details", args=[poll.id])
            )
        return polls


class DetailView(DetailView):
    model = Poll
    template_name = "polls/poll_detail.html"
    context_object_name = "poll"
    pk_url_kwarg = "poll_id"


# @require_POST
def vote(request, slot_id):
    slot = get_object_or_404(Slot, pk=slot_id)
    poll = slot.poll

    # Check poll access restrictions
    if poll.poll_type == Poll.PRIVATE or poll.poll_type != Poll.PRIVATE:
        if (
            False
            and not request.user.is_authenticated
            and request.user not in poll.invited_users.all()
        ):
            raise PermissionDenied("You are not invited to vote on this private poll.")

    elif poll.poll_type == Poll.SEMI and not request.user.is_authenticated:
        raise PermissionDenied("You must be logged in to vote on this poll.")

    voter_name = request.POST.get("voter_name")
    if voter_name:
        Vote.objects.get_or_create(slot=slot, voter_name=voter_name)

    if request.headers.get("HX-Request"):
        return render(request, "polls/partials/vote_count.html", {"slot": slot})

    return redirect("polls:details", poll_id=poll.id)


@login_required  # recommended if you use authentication
def close_poll(request, poll_id, slot_id):
    poll = get_object_or_404(Poll, id=poll_id)
    slot = get_object_or_404(Slot, id=slot_id, poll=poll)

    poll.is_closed = True
    poll.selected_slot = slot
    Validate(poll)
    poll.save()

    return redirect("polls:details", poll_id=poll.id)


def download_ics(request, poll_id):
    poll = get_object_or_404(
        Poll, id=poll_id, is_closed=True, selected_slot__isnull=False
    )

    c = Calendar()
    e = Event()
    e.name = poll.title
    e.description = poll.description
    e.begin = poll.selected_slot.datetime
    e.duration = {"hours": 1}  # default to 1 hour; adjust as needed
    c.events.add(e)

    response = HttpResponse(str(c), content_type="text/calendar")
    response["Content-Disposition"] = f'attachment; filename="calendar_entry.ics"'

    return response

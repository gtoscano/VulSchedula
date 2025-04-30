from .models import Poll, Slot, Vote

from SerializeData import isSerializable


def Validate(poll):
    if isSerializable([poll.title, poll.description, poll.selected_slot.datetime]):
        return True
    else:
        return False

from django.contrib import admin
from .models import Poll, Slot, Vote

class SlotInline(admin.TabularInline):
    model = Slot

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator_name', 'poll_type', 'created_at', 'is_closed')
    inlines = [SlotInline]
    filter_horizontal = ('invited_users',)

admin.site.register(Slot)
admin.site.register(Vote)

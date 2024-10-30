from django.contrib import admin
from guardian.admin import GuardedModelAdmin

from .models import Ticket, Review


class TicketAdmin(GuardedModelAdmin):
    # Specify fields to show in the list view
    list_display = (
        "title",
        "user",
        "time_created",
    )


class ReviewAdmin(admin.ModelAdmin):
    # Specify fields to show in the list view
    list_display = (
        "headline",
        "rating",
        "user",
        "time_created",
    )


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)

from django.contrib import admin

from .models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):
    # Specify fields to show in the list view
    list_display = (
        "title",
        "user",
        "time_created",
    )
    # search_fields = ("name",)  # Add search functionality
    # list_filter = ("price",)  # Add filter options
    # ordering = ("name",)  # Set default ordering
    
class ReviewAdmin(admin.ModelAdmin):
    # Specify fields to show in the list view
    list_display = (
        "headline",
        "rating",
        "user",
        "time_created",
    )
    # search_fields = ("name",)  # Add search functionality
    # list_filter = ("price",)  # Add filter options
    # ordering = ("name",)  # Set default ordering


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)

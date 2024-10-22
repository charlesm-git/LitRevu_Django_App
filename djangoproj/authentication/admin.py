from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    # Specify fields to show in the list view
    list_display = ("username",)
    # search_fields = ("name",)  # Add search functionality
    # list_filter = ("price",)  # Add filter options
    # ordering = ("name",)  # Set default ordering


admin.site.register(User, UserAdmin)

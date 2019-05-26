from django.contrib import admin

from complaint.models import Complaint


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    pass

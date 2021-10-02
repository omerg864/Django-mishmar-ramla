from django.contrib import admin
from .models import Shift1 as Shift
from .models import Post
from .models import Event
from .models import Organization as Organization
from .models import IpBan

admin.site.register(Shift)


class OrganizationAdmin(admin.ModelAdmin):
    fields = ("date", )


class EventAdmin(admin.ModelAdmin):
    list_display = ("date2", "nickname", "description", "training", "night_before", "morning", "after_noon", "night")


admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Post)
admin.site.register(Event, EventAdmin)
admin.site.register(IpBan)
# Register your models here.

from django.contrib import admin
from .models import Shift1 as Shift
from .models import Post
from .models import Event
from .models import Organization as Organization
from .models import IpBan
from .models import Week
from .models import ShiftWeek
from .models import Gun
from .models import Arming_Log
from .models import ValidationLog
from .models import ArmingRequest

admin.site.register(Shift)
admin.site.register(ShiftWeek)


class OrganizationAdmin(admin.ModelAdmin):
    fields = ("date", )


class EventAdmin(admin.ModelAdmin):
    list_display = ("date2", "nickname", "description", "training", "night_before", "morning", "after_noon", "night")


admin.site.register(Organization)
admin.site.register(Post)
admin.site.register(Week)
admin.site.register(Event, EventAdmin)
admin.site.register(IpBan)
admin.site.register(Gun)
admin.site.register(Arming_Log)
admin.site.register(ValidationLog)
admin.site.register(ArmingRequest)
# Register your models here.

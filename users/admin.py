from django.contrib import admin
from .models import Profile2 as Profile
from django.contrib.auth.models import User

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('user', "name", 'nickname',
                    'night', 'sat_night', 'sat_morning', 'sat_noon')
    list_editable = ('nickname', 'night', 'sat_night', 'sat_morning', 'sat_noon')
    search_fields = ['=user__username', ]

    def name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'


admin.site.register(Profile, ProfileAdmin)

from django import forms
from users.models import Profile as Profile
from .models import Settings3 as Settings
from .models import Shift1 as Shift
from .models import Organization2 as Organization
from django.contrib.auth.models import User


class QualityUpdateForm(forms.ModelForm):
    night = forms.IntegerField(min_value=0)
    sat_night = forms.IntegerField(min_value=0)
    sat_morning = forms.IntegerField(min_value=0)
    sat_noon = forms.IntegerField(min_value=0)

    class Meta:
        model = Profile
        fields = ['user', 'night', 'sat_night', 'sat_morning', 'sat_noon']


class OrganizationUpdateForm(forms.ModelForm):

    class Meta:
        fields_temp = []
        for i in range(1, 15):
            fields_temp.append("Day" + str(i) + "_630")
            fields_temp.append("Day" + str(i) + "_700_search")
            fields_temp.append("Day" + str(i) + "_700_manager")
            fields_temp.append("Day" + str(i) + "_720_1")
            fields_temp.append("Day" + str(i) + "_720_pull")
            fields_temp.append("Day" + str(i) + "_720_2")
            fields_temp.append("Day" + str(i) + "_720_3")
            fields_temp.append("Day" + str(i) + "_1400")
            fields_temp.append("Day" + str(i) + "_1500")
            fields_temp.append("Day" + str(i) + "_1500_1900")
            fields_temp.append("Day" + str(i) + "_2300")
            fields_temp.append("Day" + str(i) + "_notes")
        fields_temp.append("published")
        model = Organization
        fields = fields_temp


class SettingsForm(forms.ModelForm):
    submitting = forms.BooleanField(required=False)
    pin_code = forms.IntegerField(required=True)
    officer = forms.CharField(max_length=20)

    class Meta:
        model = Settings
        fields = "__all__"


class ShiftForm(forms.ModelForm):

    class Meta:
        fields_temp = []
        for i in range(1, 15):
            fields_temp.append("M" + str(i))
            fields_temp.append("A" + str(i))
            fields_temp.append("N" + str(i))
            fields_temp.append("P" + str(i))
            fields_temp.append("R" + str(i))
            fields_temp.append("notes" + str(i))
        fields_temp.append("seq_night")
        fields_temp.append("seq_noon")
        model = Shift
        fields = fields_temp


class ShiftViewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShiftViewForm, self).__init__(*args, **kwargs)
        fields_temp = []
        for i in range(1, 15):
            fields_temp.append("M" + str(i))
            fields_temp.append("A" + str(i))
            fields_temp.append("N" + str(i))
            fields_temp.append("P" + str(i))
            fields_temp.append("R" + str(i))
            fields_temp.append("notes" + str(i))
        fields_temp.append("seq_night")
        fields_temp.append("seq_noon")
        for field in fields_temp:
            self.fields[field].disabled = True

    class Meta:
        fields_temp = []
        for i in range(1, 15):
            fields_temp.append("M" + str(i))
            fields_temp.append("A" + str(i))
            fields_temp.append("N" + str(i))
            fields_temp.append("P" + str(i))
            fields_temp.append("R" + str(i))
            fields_temp.append("notes" + str(i))
        fields_temp.append("seq_night")
        fields_temp.append("seq_noon")
        model = Shift
        fields = fields_temp
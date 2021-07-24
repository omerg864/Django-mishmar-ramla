import datetime
import io
import random
import xlsxwriter as xlsxwriter
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User, Group
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.template.defaulttags import register
from django.views.generic import UpdateView, ListView, DetailView
from .backend.Schedule.Organizer import Organizer
from .forms import SettingsForm, ShiftForm, ShiftViewForm, OrganizationUpdateForm
from .models import Post
from .models import Settings as Settings
from .models import Shift1 as Shift
from .models import Event
from .models import Organization2 as Organization
from users.models import Profile as Profile
from django.utils.translation import activate
import openpyxl
import requests

activate('he')

if len(Settings.objects.all()) == 0:
    new_settings = Settings(submitting=True, pin_code=1234, officer="")
    new_settings.save()

data = {}
api_key = "4cba4792d5c0c0222cc84e409138af7a"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = "Ramla"
try:
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    data = response.json()
except ConnectionError:
    data = {"Not Found:": ""}

if data["cod"] != "404":
    try:
        y = data["main"]
        current_temperature = str(int(y["temp"] - 273.15)) + " °C"
        current_pressure = str(y["pressure"]) + " hPa"
        current_humidiy = str(y["humidity"]) + "%"
        weather_description = data["weather"][0]["description"]
        weather = {
            "Temperature": current_temperature,
            "Atmospheric Pressure": current_pressure,
            "Humidity": current_humidiy,
            "Description": weather_description
        }
    except AttributeError:
        print("Weather Error")
        weather = {
            "Not Found": "לא ניתן לטעון מזג האוויר"
        }

else:
    print(" City Not Found ")
    weather = {
        "Not Found": "עיר לא נמצא"
    }


@staff_member_required
def settings_view(request):
    settings = Settings.objects.all().last()
    if request.method == 'POST':
        settings_form = SettingsForm(request.POST, instance=settings)
        if settings_form.is_valid():
            messages.success(request, f'שינויים נשמרו!')
            settings_form.save()
        else:
            messages.error(request, f'שינויים לא נשמרו!')
    else:
        settings_form = SettingsForm(instance=settings)
    context = {
        "settings_form": settings_form
    }
    return render(request, "Schedule/settings.html", context)


def home(request):
    posts = Post.objects.all()
    context = {
        "weather": weather,
        "posts": posts,
    }
    return render(request, "Schedule/Home.html", context)


def error_404_view(request, exception):
    return render(request, 'Schedule/404.html')


@login_required
def shift_view(request):
    form = None
    days = {}
    notes_text = ""
    empty = False
    settings = Settings.objects.last()
    submitting = settings.submitting
    for x in range(14):
        days["day" + str(x)] = Organization.objects.order_by('-date')[0].date + datetime.timedelta(days=x)
    events = Event.objects.all()
    for x in range(14):
        if len(events.filter(date2=days["day" + str(x)])) > 0:
            for ev in events.filter(date2=days["day" + str(x)]):
                if request.user.profile.nickname == ev.nickname:
                    message = f'לא לשכוח בתאריך {ev.date2} יש {ev.description}. אם יש שינוי להודיע!'
                    messages.info(request, message)
                elif ev.nickname == 'כולם':
                    message = f'לא לשכוח בתאריך {ev.date2} יש {ev.description}'
                    messages.info(request, message)
    if request.method == 'POST':
        if not already_submitted(request.user):
            form = ShiftForm(request.POST)
        else:
            last_date = Organization.objects.order_by('-date')[0].date
            shifts = Shift.objects.filter(date=last_date)
            shift = shifts.filter(username=request.user).first()
            notes_text = str(shift.notes)
            form = ShiftForm(request.POST, instance=shift)
        form.instance.username = request.user
        form.instance.date = Organization.objects.order_by('-date')[0].date
        notes_area = request.POST.get("notesArea")
        form.instance.notes = notes_area
        if form.is_valid():
            if not already_submitted(request.user):
                messages.success(request, f'משמרות הוגשו בהצלחה!')
            else:
                messages.success(request, f'משמרות עודכנו בהצלחה!')
            form.save()
            return redirect("Schedule-Home")
        else:
            messages.error(request, f'שינויים לא נשמרו!')
    else:
        if not submitting:
            shifts = Shift.objects.order_by('-date')
            if len(shifts.filter(username=request.user).order_by('-date')) > 0:
                shift = shifts.filter(username=request.user).order_by('-date')[0]
                notes_text = str(shift.notes)
                for x in range(14):
                    days["day" + str(x)] = shift.date + datetime.timedelta(days=x)
                form = ShiftViewForm(instance=shift)
            else:
                empty = True
        elif not already_submitted(request.user):
            form = ShiftForm()
        else:
            last_date = Organization.objects.order_by('-date')[0].date
            shifts = Shift.objects.filter(date=last_date)
            shift = shifts.filter(username=request.user).first()
            notes_text = str(shift.notes)
            form = ShiftForm(instance=shift)
    if not empty:
        context = {
            "form": form,
            "days": days,
            "submitting": submitting,
            "notes_text": notes_text,
            "empty": empty,
            "manager": False,
        }
    else:
        context = {
            "empty": empty,
            "manager": False,
        }
    return render(request, "Schedule/shifts.html", context)


def already_submitted(user):
    last_date = Organization.objects.order_by('-date')[0].date
    shifts = Shift.objects.filter(date=last_date)
    if len(shifts) == 0:
        return False
    else:
        if len(shifts.filter(username=user)) == 0:
            return False
        else:
            return True


def get_input(organization_last):
    organization_last_input = {}
    fields = ["_630", "_700_search", "_700_manager", "_720_1", "_720_pull", "_720_2", "_720_3", "_1400", "_1500",
              "_1500_1900", "_2300", "_notes"]
    for i in range(1, 15):
        day1 = f'Day{i}'
        day2 = f'day{i}'
        for f in fields:
            organization_last_input[day2 + f] = getattr(organization_last, day1 + f)
    return organization_last_input


class ServedSumListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Organization
    template_name = "Schedule/Served_sum_list.html"
    context_object_name = "organizations"
    ordering = ["-date"]
    paginate_by = 5

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class ShiftUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Shift
    template_name = "Schedule/shifts.html"
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
    fields = fields_temp

    def form_valid(self, form):
        self.object.notes = self.request.POST.get("notesArea")
        super(ShiftUpdateView, self).form_valid(form)
        messages.success(self.request, f'עדכון הושלם')
        return redirect("Schedule-Served-sum")

    def get_context_data(self, **kwargs):
        ctx = super(ShiftUpdateView, self).get_context_data(**kwargs)
        ctx["days"] = {}
        for x in range(14):
            ctx["days"]["day" + str(x)] = self.object.date + datetime.timedelta(days=x)
        ctx["notes_text"] = str(self.object.notes)
        ctx["submitting"] = True
        ctx["empty"] = False
        ctx["manager"] = True
        user = User.objects.filter(username=self.object.username).first()
        ctx["userview"] = user.profile.nickname
        return ctx

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class OrganizationDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    template_name = "Schedule/organization-detail.html"

    def get_context_data(self, **kwargs):
        ctx = super(OrganizationDetailView, self).get_context_data(**kwargs)
        for x in range(14):
            ctx["day" + str(x)] = self.object.date + datetime.timedelta(days=x)
        return ctx


class ShifttableView(LoginRequiredMixin, DetailView):
    model = Organization
    template_name = "Schedule/shift-table-view.html"

    def get_context_data(self, **kwargs):
        ctx = super(ShifttableView, self).get_context_data(**kwargs)
        organization = get_input(self.get_object())
        users = set()
        for key in organization:
            if key.count("notes") == 0:
                organization[key] = organization[key].replace("\r", "\n")
                split = organization[key].split("\n")
                for s in split:
                    s = s.replace(" ", "")
                    users.add(s)
        if " " in users:
            users.remove(" ")
        if "" in users:
            users.remove("")
        table_content = {}
        sum_content = {"morning1": 0, "noon1": 0, "morning2": 0, "noon2": 0, "night": 0, "end": 0}
        for user in users:
            table_content[user] = {"morning1": 0, "noon1": 0, "morning2": 0, "noon2": 0, "night": 0, "end": 0}
        morning_shifts = ["630", "700_search", "700_manager", "720_pull", "720_1", "720_2", "720_3"]
        noon_shifts = ["1400", "1500", "1500_1900"]
        for x in range(1, 15):
            day = f'day{x}_'
            for shift in morning_shifts:
                split = organization[f'{day}{shift}'].split("\n")
                for s in split:
                    s = s.replace(" ", "")
                    if s != "":
                        if x < 6:
                            table_content[s]["morning1"] += 1
                            sum_content["morning1"] += 1
                        elif 7 < x < 13:
                            table_content[s]["morning2"] += 1
                            sum_content["morning2"] += 1
                        else:
                            table_content[s]["end"] += 1
                            sum_content["end"] += 1
            for shift in noon_shifts:
                split = organization[f'{day}{shift}'].split("\n")
                for s in split:
                    s = s.replace(" ", "")
                    if s != "":
                        if x < 6:
                            table_content[s]["noon1"] += 1
                            sum_content["noon1"] += 1
                        elif 7 < x < 13:
                            table_content[s]["noon2"] += 1
                            sum_content["noon2"] += 1
                        else:
                            table_content[s]["end"] += 1
                            sum_content["end"] += 1
            split = organization[f'{day}2300'].split("\n")
            for s in split:
                s = s.replace(" ", "")
                if s != "":
                    if x != 6 and x != 7 and x != 13 and x != 14:
                        table_content[s]["night"] += 1
                        sum_content["night"] += 1
                    else:
                        table_content[s]["end"] += 1
                        sum_content["end"] += 1
        ctx["table"] = table_content
        ctx["sum"] = sum_content
        for x in range(14):
            ctx["day" + str(x)] = self.get_object().date + datetime.timedelta(days=x)
        return ctx


class ServedSumReinforcementsDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    template_name = "Schedule/served_sum_reinforcements.html"

    def get_data(self, calculated: bool):
        ctx = {}
        served = {}
        if calculated:
            organization = self.get_object()
            organization_input = get_input(organization)
            input_days = {}
            keys = ["_630", "_700_search", "_720_1", "_720_pull", "_720_2", "_720_3", "_1400", "_1500",
                    "_1500_1900",
                    "_2300"]
        for i in range(1, 15):
            served["day" + str(i)] = ""
            if calculated:
                day = "day" + str(i)
                input_days[day + "M"] = []
                input_days[day + "A"] = []
                input_days[day + "N"] = []
                for x in range(10):
                    if x < 6:
                        input_days[day + "M"] += organization_input[day + keys[x]].split("\n")
                    elif x < 9:
                        input_days[day + "A"] += organization_input[day + keys[x]].split("\n")
                    else:
                        input_days[day + "N"] += organization_input[day + keys[x]].split("\n")
        if calculated:
            for key in input_days:
                for i in range(len(input_days[key])):
                    input_days[key][i] = input_days[key][i].replace(" ", "")
                    input_days[key][i] = input_days[key][i].replace("\n", "")
                    input_days[key][i] = input_days[key][i].replace("\r", "")
        shift_date = self.get_object().date
        shifts_served = Shift.objects.all().filter(date=shift_date)
        notes = {"general": "", "week1": "", "week2": ""}
        users = {}
        for shift in shifts_served:
            username = shift.username
            user = User.objects.all().filter(username=username).first()
            users[user.profile.nickname] = shift.id
            name = user.profile.nickname
            index = 1
            shifts = [shift.R1, shift.R2, shift.R3, shift.R4, shift.R5, shift.R6, shift.R7, shift.R8, shift.R9,
                      shift.R10, shift.R11, shift.R12, shift.R13, shift.R14]
            for s in shifts:
                if s:
                    served["day" + str(index)] = served["day" + str(index)] + name
                index += 1
            notes1 = [shift.notes1, shift.notes2, shift.notes3,
                      shift.notes4, shift.notes5, shift.notes6, shift.notes7]
            index = 1
            for n in notes1:
                if n != "":
                    notes["week1"] = notes["week1"] + name + ": " \
                                     + number_to_day2(index) + " - " + n + "\n"
                index += 1
            notes2 = [shift.notes8, shift.notes9, shift.notes10,
                      shift.notes11, shift.notes12, shift.notes13, shift.notes14]
            index = 1
            for n in notes2:
                if n != "":
                    notes["week2"] = notes["week2"] + name + ": " \
                                     + number_to_day2(index) + " - " + n + "\n"
                index += 1
            if shift.notes != "":
                notes["general"] = notes["general"] + name + ": " + shift.notes + "\n"
        days = {}
        for x in range(14):
            days["day" + str(x)] = self.get_object().date + datetime.timedelta(days=x)
        ##
        # Calculated Part
        if calculated:
            calc_served = {}
            for x in range(1, 15):
                day = "day" + str(x)
                calc_served[day] = ""
                split = served[day].split("\n")
                for s in split:
                    if s not in input_days[day + "A"] and s != "" and s != " " and s != "\n":
                        day_before = "day" + str(x - 1)
                        day_after = "day" + str(x + 1)
                        if x != 1 and x != 14:
                            if s not in input_days[day + "M"] and s not in input_days[day + "N"] and \
                                    s not in input_days[day_before + "N"] and s not in input_days[day_after + "M"]:
                                calc_served[day] += s + "\n"
                            elif s not in input_days[day + "M"] and s not in input_days[day_before + "N"] \
                                    and s not in input_days[day + "N"]:
                                calc_served[day] += s + "\n" + " (יכול בוקר וצהריים) " + "\n"
                            elif s not in input_days[day + "M"] and s not in input_days[day_before + "N"]:
                                calc_served[day] += s + "\n" + " (יכול רק בוקר) " + "\n"
                            elif s not in input_days[day + "M"] and s not in input_days[day_after + "M"] \
                                    and s not in input_days[day + "N"]:
                                calc_served[day] += s + "\n" + " (יכול רק צהריים ולילה) " + "\n"
                            elif s not in input_days[day + "N"] and s not in input_days[day_after + "M"]:
                                calc_served[day] += s + "\n" + " (יכול רק לילה) " + "\n"
                        elif x == 1:
                            if s not in input_days[day + "M"] and s not in input_days[day + "N"] and \
                                    s not in input_days[day_after + "M"]:
                                calc_served[day] += s + "\n"
                            elif s not in input_days[day + "M"] and s not in input_days[day + "N"]:
                                calc_served[day] += s + "\n" + " (יכול בוקר וצהריים) " + "\n"
                            elif s not in input_days[day + "M"] and s not in input_days[day_after + "M"] \
                                    and s not in input_days[day + "N"]:
                                calc_served[day] += s + "\n" + " (יכול רק צהריים ולילה) " + "\n"
                            elif s not in input_days[day + "N"] and s not in input_days[day_after + "M"]:
                                calc_served[day] += s + "\n" + " (יכול רק לילה) " + "\n"
                            elif s not in input_days[day + "M"]:
                                calc_served[day] += s + "\n" + " (יכול רק בוקר) " + "\n"
                        else:
                            if s not in input_days[day + "M"] and s not in input_days[day + "N"] and \
                                    s not in input_days[day_before + "N"]:
                                calc_served[day] += s + "\n"
                            elif s not in input_days[day + "M"] and s not in input_days[day_before + "N"] \
                                    and s not in input_days[day + "N"]:
                                calc_served[day] += s + "\n" + " (יכול בוקר וצהריים) " + "\n"
                            elif s not in input_days[day + "M"] and s not in input_days[day_before + "N"]:
                                calc_served[day] += s + "\n" + " (יכול רק בוקר) " + "\n"
                            elif s not in input_days[day + "M"] and s not in input_days[day + "N"]:
                                calc_served[day] += s + "\n" + " (יכול רק צהריים ולילה) " + "\n"
                            elif s not in input_days[day + "N"]:
                                calc_served[day] += s + "\n" + " (יכול רק לילה) " + "\n"
            served = calc_served
        ctx["calculated"] = calculated
        ctx["days"] = days
        ctx["served"] = served
        ctx["notes"] = notes
        ctx["num_served"] = len(shifts_served)
        ctx["users"] = users
        return ctx

    def get_context_data(self, **kwargs):
        ctx = super(ServedSumReinforcementsDetailView, self).get_context_data(**kwargs)
        calculated = False
        context = self.get_data(calculated)
        for c in context:
            ctx[c] = context[c]
        return ctx

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            calculated = True
            if 'calculated' in request.POST:
                if request.POST.get("calculated") == "True":
                    calculated = False
                else:
                    calculated = True
            ctx = self.get_data(calculated)
            return render(request, "Schedule/served_sum_reinforcements.html", ctx)


class ServedSumShiftDetailView(LoginRequiredMixin, DetailView):
    model = Organization
    template_name = "Schedule/Served-sum.html"

    def get_data(self):
        ctx = {}
        served = {}
        for i in range(1, 15):
            served["M" + str(i)] = ""
            served["A" + str(i)] = ""
            served["N" + str(i)] = ""
        shift_date = self.get_object().date
        shifts_served = Shift.objects.all().filter(date=shift_date)
        notes = {"general": "", "week1": "", "week2": ""}
        users = {}
        for shift in shifts_served:
            username = shift.username
            user = User.objects.all().filter(username=username).first()
            users[user.profile.nickname] = shift.id
            name = user.profile.nickname
            name = name.replace("\n", "")
            name = name.replace("\r", "")
            kind = "M"
            morning = False
            count = 0
            index = 1
            shifts = [shift.M1, shift.P1, shift.A1, shift.N1, shift.M2, shift.P2, shift.A2, shift.N2, shift.M3,
                      shift.P3,
                      shift.A3, shift.N3, shift.M4, shift.P4, shift.A4, shift.N4, shift.M5, shift.P5, shift.A5,
                      shift.N5,
                      shift.M6, shift.P6, shift.A6, shift.N6, shift.M7, shift.P7, shift.A7, shift.N7, shift.M8,
                      shift.P8,
                      shift.A8, shift.N8, shift.M9, shift.P9, shift.A9, shift.N9, shift.M10, shift.P10, shift.A10,
                      shift.N10, shift.M11, shift.P11, shift.A11, shift.N11, shift.M12, shift.P12, shift.A12, shift.N12,
                      shift.M13, shift.P13, shift.A13, shift.N13, shift.M14, shift.P14, shift.A14, shift.N14]
            for s in shifts:
                if s:
                    if count == 0:
                        morning = True
                        served[kind + str(index)] = served[kind + str(index)] + name
                    else:
                        if count == 1:
                            if morning:
                                served[kind + str(index)] = served[kind + str(index)] + "\n"
                            morning = False
                        else:
                            if count == 2:
                                kind = "A"
                            elif count == 3:
                                kind = "N"
                            served[kind + str(index)] = served[kind + str(index)] + name + "\n"
                else:
                    if count == 1 and morning:
                        morning = False
                        served[kind + str(index)] = served[kind + str(index)] + "\n" + "(לא משיכה)" + "\n"
                if count == 3:
                    count = 0
                    index = index + 1
                    kind = "M"
                else:
                    count = count + 1
            notes1 = [shift.notes1, shift.notes2, shift.notes3,
                      shift.notes4, shift.notes5, shift.notes6, shift.notes7]
            index = 1
            for n in notes1:
                if n != "":
                    notes["week1"] = notes["week1"] + name + ": " \
                                     + number_to_day2(index) + " - " + n + "\n"
                index += 1
            notes2 = [shift.notes8, shift.notes9, shift.notes10,
                      shift.notes11, shift.notes12, shift.notes13, shift.notes14]
            index = 1
            for n in notes2:
                if n != "":
                    notes["week2"] = notes["week2"] + name + ": " \
                                     + number_to_day2(index) + " - " + n + "\n"
                index += 1
            if shift.notes != "":
                notes["general"] = notes["general"] + name + ": " + shift.notes + "\n"
        days = {}
        for x in range(14):
            days["day" + str(x)] = self.get_object().date + datetime.timedelta(days=x)
        ctx["days"] = days
        ctx["served"] = served
        ctx["notes"] = notes
        ctx["num_served"] = len(shifts_served)
        ctx["users"] = users
        return ctx

    def get_context_data(self, **kwargs):
        ctx = super(ServedSumShiftDetailView, self).get_context_data(**kwargs)
        context = self.get_data()
        for c in context:
            ctx[c] = context[c]
        return ctx

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            ctx = self.get_data()
            return WriteToExcel(ctx["served"], ctx["notes"], ctx["days"])


class OrganizationUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Organization
    template_name = "Schedule/organization_update.html"
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
    fields = fields_temp

    def form_valid(self, form):
        super(OrganizationUpdateView, self).form_valid(form)
        messages.success(self.request, f'עדכון הושלם')
        return HttpResponseRedirect(self.request.path_info)

    def get_context_data(self, **kwargs):
        ctx = super(OrganizationUpdateView, self).get_context_data(**kwargs)
        for x in range(14):
            ctx["day" + str(x)] = self.object.date + datetime.timedelta(days=x)
        ctx["organization_id"] = self.object.id
        return ctx

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            if 'check1' in request.POST:
                form = OrganizationUpdateForm(request.POST, instance=self.get_object())
                if form.is_valid():
                    self.object = form.save()
                    messages.success(self.request, f'עדכון הושלם')
                    self.organization_valid()
                    return HttpResponseRedirect(self.request.path_info)
                else:
                    messages.info(self.request, f'תקלה טכנית לא ניתן לבדוק')
            elif 'update' in request.POST:
                form = OrganizationUpdateForm(request.POST, instance=self.get_object())
                if form.is_valid():
                    self.object = form.save()
                    messages.success(self.request, f'עדכון הושלם')
                else:
                    messages.info(self.request, f'עדכון לא הושלם תקלה טכנית')
                return HttpResponseRedirect(self.request.path_info)
            elif 'upload' in request.POST:
                self.uplaod_organize(request)
                return HttpResponseRedirect(self.request.path_info)
            elif 'table' in request.POST:
                return redirect("organization-table-shift", self.get_object().id)
            elif 'clear' in request.POST:
                form = OrganizationUpdateForm(request.POST, instance=self.get_object())
                form.data._mutable = True
                fields_temp = []
                for i in range(1, 15):
                    form.data["Day" + str(i) + "_630"] = ""
                    form.data["Day" + str(i) + "_700_search"] = ""
                    form.data["Day" + str(i) + "_700_manager"] = ""
                    form.data["Day" + str(i) + "_720_1"] = ""
                    form.data["Day" + str(i) + "_720_pull"] = ""
                    form.data["Day" + str(i) + "_720_2"] = ""
                    form.data["Day" + str(i) + "_720_3"] = ""
                    form.data["Day" + str(i) + "_1400"] = ""
                    form.data["Day" + str(i) + "_1500"] = ""
                    form.data["Day" + str(i) + "_1500_1900"] = ""
                    form.data["Day" + str(i) + "_2300"] = ""
                form.data._mutable = False
                if form.is_valid():
                    self.object = form.save()
                    messages.success(self.request, f'איפוס הושלם')
                else:
                    messages.info(self.request, f'איפוס לא הושלם תקלה טכנית')
                return HttpResponseRedirect(self.request.path_info)

    def organization_valid(self):
        organization1 = get_input(self.get_object())
        input_days = {}
        valid = True
        keys = ["_630", "_700_search", "_720_1", "_720_pull", "_720_2", "_720_3", "_1400", "_1500",
                "_1500_1900",
                "_2300"]
        for i in range(1, 15):
            day = "day" + str(i)
            input_days[day + "M"] = []
            input_days[day + "A"] = []
            input_days[day + "N"] = []
            for x in range(10):
                if x < 6:
                    input_days[day + "M"] += organization1[day + keys[x]].split("\n")
                elif x < 9:
                    input_days[day + "A"] += organization1[day + keys[x]].split("\n")
                else:
                    input_days[day + "N"] += organization1[day + keys[x]].split("\n")
        for key in input_days:
            for i in range(len(input_days[key])):
                input_days[key][i] = input_days[key][i].replace(" ", "")
                input_days[key][i] = input_days[key][i].replace("\n", "")
                input_days[key][i] = input_days[key][i].replace("\r", "")
        users = []
        for u in User.objects.all():
            users.append(u.profile.nickname)
        for name in users:
            for x in range(1, 15):
                message1 = name + " ביום ה-" + str(x) + " בשתי משמרות רצופות"
                message2 = name + " ביום ה-" + str(x) + " באותה משמרת פעמיים"
                day = "day" + str(x)
                day_before = "day" + str(x - 1)
                day_after = "day" + str(x + 1)
                if name in input_days[day + "M"]:
                    if is_more_than_once(input_days[day + "M"], name):
                        messages.info(self.request, message2)
                        valid = False
                    if x != 1:
                        if name in input_days[day + "A"] or name in input_days[day_before + "N"]:
                            messages.info(self.request, message1)
                            valid = False
                    else:
                        if name in input_days[day + "A"]:
                            messages.info(self.request, message1)
                            valid = False
                if name in input_days[day + "A"]:
                    if is_more_than_once(input_days[day + "A"], name):
                        messages.info(self.request, message2)
                        valid = False
                    if name in input_days[day + "M"] or name in input_days[day + "N"]:
                        messages.info(self.request, message1)
                        valid = False
                if name in input_days[day + "N"]:
                    if is_more_than_once(input_days[day + "N"], name):
                        messages.info(self.request, message2)
                        valid = False
                    if x != 14:
                        if name in input_days[day + "A"] or name in input_days[day_after + "M"]:
                            messages.info(self.request, message1)
                            valid = False
                    else:
                        if name in input_days[day + "A"]:
                            messages.info(self.request, message1)
                            valid = False
        if valid:
            messages.success(self.request, "סידור תקין")

    def extract_data(self, request):
        # extract from excel
        myfile = request.FILES['myfile']
        file_object = myfile.file
        wb = openpyxl.load_workbook(file_object)
        sheet = wb.active
        ## Green background FFC6EFCE
        ## Green font FF006100
        ## Red background FFFFC7CE
        ## Red font with red background FF9C0006
        ## White background 00000000
        ## Black font Values must be of type <class 'str'> rgb=None, indexed=None, auto=None, theme=1, tint=0.0, type='theme'
        ## Red font FFFF0000
        ## Empty font Values must be of type <class 'str'> rgb=None, indexed=None, auto=None, theme=1, tint=0.0, type='theme'
        ## Empty value None
        ## orange background FFFFEB9C
        # print(str(sheet.cell(10, 3).value))
        # print(str(sheet.cell(10, 3).font.color.rgb))  # Get the font color in the table
        # print(str(sheet.cell(10, 3).fill.fgColor.rgb)) # background color
        # if str(sheet.cell(10, 3).font.color.rgb) == "Values must be of type <class 'str'>":
        end_morning_str = ""
        end_noon_str = ""
        end_night_str = ""
        for rng in sheet.merged_cells.ranges:
            if 'A5' in rng:
                end_morning_str = str(rng)
                break
        end_morning_str = end_morning_str.replace("A5:A", "")
        end_morning = int(end_morning_str)
        for rng in sheet.merged_cells.ranges:
            if f'A{end_morning + 1}' in rng:
                end_noon_str = str(rng)
                break
        end_noon_str = end_noon_str.replace(f'A{end_morning + 1}:A', "")
        end_noon = int(end_noon_str)
        for rng in sheet.merged_cells.ranges:
            if f'A{end_noon + 1}' in rng:
                end_night_str = str(rng)
                break
        end_night_str = end_night_str.replace(f'A{end_noon + 1}:A', "")
        end_night = int(end_night_str)
        col = 1
        names_days = {}
        no_pull_names = {}
        for x in range(14):
            col += 1
            names_days[f'day{x}_morning'] = []
            no_pull_names[f'day{x}'] = []
            names_days[f'day{x}_noon'] = []
            names_days[f'day{x}_night'] = []
            for j in range(5, end_morning + 1):
                if str(sheet.cell(j, col).fill.fgColor.rgb) == 'FFC6EFCE' \
                        or str(sheet.cell(j, col).fill.fgColor.rgb) == 'FFFFEB9C':
                    names_days[f'day{x}_morning'].append(str(sheet.cell(j, col).value))
                    if str(sheet.cell(j, col).fill.fgColor.rgb) == 'FFFFEB9C':
                        no_pull_names[f'day{x}'].append(str(sheet.cell(j, col).value))
            for j in range(end_morning + 1, end_noon + 1):
                if str(sheet.cell(j, col).fill.fgColor.rgb) == 'FFC6EFCE':
                    names_days[f'day{x}_noon'].append(str(sheet.cell(j, col).value))
            for j in range(end_noon + 1, end_night + 1):
                if str(sheet.cell(j, col).fill.fgColor.rgb) == 'FFC6EFCE':
                    names_days[f'day{x}_night'].append(str(sheet.cell(j, col).value))
        # extract from database
        shifts = Shift.objects.all().filter(date=self.get_object().date)
        users = User.objects.all()
        max_seq0 = 2
        max_seq1 = 2
        sequence_count = {}
        max_out_names = [[], []]
        for s in shifts:
            name = users.filter(username=s.username).first().profile.nickname
            sequence_count[f'{name}0'] = s.seq_night
            sequence_count[f'{name}1'] = s.seq_noon
            if sequence_count[f'{name}0'] >= max_seq0:
                max_out_names[0].append(name)
            if sequence_count[f'{name}1'] >= max_seq1:
                max_out_names[1].append(name)
        return [names_days, no_pull_names, sequence_count, max_out_names, max_seq0, max_seq1]

    def search_and_put(self, form, for_list, check_list, day, time, max_out_names, seq,
                       sequence_count, max_seq0, max_seq1, is_seq, extra_seq):
        if seq == 0:
            max_seq = max_seq0
        else:
            max_seq = max_seq1
        for name in for_list:
            if name in check_list and name not in extra_seq:
                if is_seq:
                    if name not in max_out_names:
                        if f'{name}{seq}' in sequence_count.keys():
                            sequence_count[f'{name}{seq}'] += 1
                            if sequence_count[f'{name}{seq}'] >= max_seq:
                                max_out_names.append(name)
                        if form.data[f'Day{day + 1}_{time}'] == "":
                            form.data[f'Day{day + 1}_{time}'] = name
                        else:
                            form.data[f'Day{day + 1}_{time}'] += "\n" + name
                        check_list.remove(name)
                        return True
                else:
                    if form.data[f'Day{day + 1}_{time}'] == "":
                        form.data[f'Day{day + 1}_{time}'] = name
                    else:
                        form.data[f'Day{day + 1}_{time}'] += "\n" + name
                    check_list.remove(name)
                    return True
        return False

    def insert_all_to_form(self, form, for_list, day, time):
        count = 0
        for name in for_list:
            if count == 0:
                form.data[f'Day{day + 1}_{time}'] = name
            else:
                form.data[f'Day{day + 1}_{time}'] += "\n" + name
            for_list.remove(name)
            count += 1

    def seperate_list(self, shift, max_out_names):
        new_list = []
        for s in shift:
            if s not in max_out_names:
                new_list.append(s)
        return new_list

    def insert_random(self, form, list1, time, day, count):
        if len(list1) > 0:
            r = random.randint(0, len(list1) - 1)
            if count == 0:
                form.data[f'Day{day + 1}_{time}'] = list1[r]
            else:
                form.data[f'Day{day + 1}_{time}'] += "\n" + list1[r]
            return list1.pop(r)
        else:
            return None

    def uplaod_organize(self, request):
        extracted_data = self.extract_data(request)
        names_days = extracted_data[0]
        no_pull_names = extracted_data[1]
        sequence_count = extracted_data[2]
        max_out_names = extracted_data[3]
        max_seq0 = extracted_data[4]
        max_seq1 = extracted_data[5]
        before_organization = Organization.objects.all().filter(
            date=self.get_object().date - datetime.timedelta(days=14)).first()
        if before_organization is not None:
            before_names = {"motsash": before_organization.Day14_2300.split("\n"),
                            "noon": before_organization.Day14_1500.split("\n"),
                            "morning": before_organization.Day14_630.split("\n") +
                                       before_organization.Day14_700_search.split("\n") +
                                       before_organization.Day14_700_manager.split("\n") +
                                       before_organization.Day14_720_1.split("\n")}
            for key in before_names:
                for v in before_names[key]:
                    if v == '' or v == '\r' or v == ' ':
                        count = before_names[key].count(v)
                        for x in range(count):
                            before_names[key].remove(v)
                    else:
                        before_names[key][before_names[key].index(v)] = v.replace("\r", "")
        else:
            before_names = {"motsash": [], "noon": [], "morning": []}
        form = OrganizationUpdateForm(request.POST, instance=self.get_object())
        form.data._mutable = True
        manager_group = Group.objects.filter(name="manager").first()
        manager_group_users = User.objects.filter(groups=manager_group)
        managers = []
        for m in manager_group_users:
            managers.append(m.profile.nickname)
        for x in range(13, -1, -1):
            if x != 5 and x != 6 and x != 12 and x != 13:
                is_manager = False
                for name in managers:
                    if name in names_days[f'day{x}_morning']:
                        form.data[f'Day{x + 1}_700_manager'] = name
                        names_days[f'day{x}_morning'].remove(name)
                        is_manager = True
                        break
                if not is_manager:
                    if Settings.objects.last().officer in names_days[f'day{x}_morning']:
                        form.data[f'Day{x + 1}_700_manager'] = Settings.objects.last().officer
                        names_days[f'day{x}_morning'].remove(Settings.objects.last().officer)
                temp_morning = []
                if len(names_days[f'day{x}_morning']) > 0:
                    for name in names_days[f'day{x}_morning']:
                        temp_morning.append(name)
                    for name in temp_morning:
                        if name in no_pull_names[f'day{x}'] or name in names_days[f'day{x}_night']:
                            if x == 0:
                                temp_morning.remove(name)
                            elif name in names_days[f'day{x - 1}_noon']:
                                temp_morning.remove(name)
                    if len(temp_morning) > 0:
                        inserted = self.insert_random(form, temp_morning, "720_pull", x, 0)
                        names_days[f'day{x}_morning'].remove(inserted)
                    else:
                        temp_morning = []
                        for name in names_days[f'day{x}_morning']:
                            temp_morning.append(name)
                        for name in temp_morning:
                            if x != 0:
                                if name in names_days[f'day{x - 1}_noon']:
                                    temp_morning.remove(name)
                            else:
                                if name in before_names["noon"] or name in before_names["morning"]:
                                    temp_morning.remove(name)
                        if len(temp_morning) > 0:
                            inserted = self.insert_random(form, temp_morning, "720_pull", x, 0)
                            names_days[f'day{x}_morning'].remove(inserted)
                        else:
                            self.insert_random(form, names_days[f'day{x}_morning'], "720_pull", x, 0)
                chosen = False
                if x == 0:
                    chosen = self.search_and_put(form, before_names["noon"], names_days[f'day{x}_morning'], x,
                                                 "630", max_out_names[0], 0, sequence_count, max_seq0,
                                                 max_seq1, True, [])
                    if not chosen:
                        chosen = self.search_and_put(form, before_names["morning"], names_days[f'day{x}_morning'], x,
                                                     "630", max_out_names[0], 0, sequence_count, max_seq0,
                                                     max_seq1, True, [])
                    if not chosen:
                        temp_morning = self.seperate_list(names_days[f'day{x}_morning'], max_out_names)
                        if len(temp_morning) > 0:
                            chosen = self.insert_random(form, temp_morning, "630", x, 0)
                            if chosen is not None:
                                names_days[f'day{x}_morning'].remove(chosen)
                        else:
                            self.insert_random(form, names_days[f'day{x}_morning'], "630", x, 0)
                    chosen = self.search_and_put(form, before_names["noon"], names_days[f'day{x}_morning'], x,
                                                 "700_search", max_out_names[0], 0, sequence_count, max_seq0,
                                                 max_seq1, False, [])
                    if not chosen:
                        chosen = self.search_and_put(form, before_names["morning"], names_days[f'day{x}_morning'], x,
                                                     "700_search", max_out_names[0], 0, sequence_count, max_seq0,
                                                     max_seq1, False, [])
                    if not chosen:
                        self.insert_random(form, names_days[f'day{x}_morning'], "700_search", x, 0)
                    count = 0
                    for name in before_names["motsash"]:
                        if name in names_days[f'day{x}_noon'] and name not in max_out_names[0]:
                            if f'{name}0' in sequence_count.keys():
                                sequence_count[f'{name}0'] += 1
                                if sequence_count[f'{name}0'] >= max_seq0:
                                    max_out_names[0].append(name)
                            if count == 0:
                                form.data[f'Day{x + 1}_1400'] = name
                            else:
                                form.data[f'Day{x + 1}_1400'] += "\n" + name
                            names_days[f'day{x}_noon'].remove(name)
                            count += 1
                            if count == 2:
                                break
                    if count < 2:
                        for name in names_days[f'day{x}_noon']:
                            if count == 0:
                                form.data[f'Day{x + 1}_1400'] = name
                            else:
                                form.data[f'Day{x + 1}_1400'] += "\n" + name
                            names_days[f'day{x}_noon'].remove(name)
                            count += 1
                            if count == 2:
                                break
                    # noon
                    self.insert_all_to_form(form, names_days[f'day{x}_noon'], x, "1500")
                    # night
                    self.insert_all_to_form(form, names_days[f'day{x}_night'], x, "2300")
                # morning 630 and 700 search
                else:
                    if x > 1:
                        temp_morning = []
                        for name in names_days[f'day{x}_morning']:
                            temp_morning.append(name)
                        chosen = self.search_and_put(form, names_days[f'day{x - 1}_noon'], names_days[f'day{x}_morning']
                                                     , x, "630", max_out_names[1], 1, sequence_count, max_seq0,
                                                     max_seq1, True, names_days[f'day{x - 2}_night'])
                    else:
                        chosen = self.search_and_put(form, names_days[f'day{x - 1}_noon'],
                                                     names_days[f'day{x}_morning'], x,
                                                     "630", max_out_names[1], 1, sequence_count, max_seq0,
                                                     max_seq1, True, [])
                    if not chosen:
                        temp_morning = self.seperate_list(names_days[f'day{x}_morning'], max_out_names)
                        if len(temp_morning) > 0:
                            chosen = self.insert_random(form, temp_morning, "630", x, 0)
                            if chosen is not None:
                                names_days[f'day{x}_morning'].remove(chosen)
                        else:
                            self.insert_random(form, names_days[f'day{x}_morning'], "630", x, 0)
                    chosen = self.search_and_put(form, names_days[f'day{x - 1}_noon'], names_days[f'day{x}_morning'], x,
                                                 "700_search", max_out_names[1], 1, sequence_count, max_seq0,
                                                 max_seq1, False, [])
                    if not chosen and len(names_days[f'day{x}_morning']) > 0:
                        chosen = self.insert_random(form, names_days[f'day{x}_morning'], "700_search", x, 0)
                    # noon
                    count = 0
                    if len(names_days[f'day{x}_noon']) > 2:
                        for name in names_days[f'day{x}_noon']:
                            if name in names_days[f'day{x - 1}_night'] and name not in max_out_names[0]:
                                if f'{name}0' in sequence_count.keys():
                                    sequence_count[f'{name}0'] += 1
                                    if sequence_count[f'{name}0'] >= max_seq0:
                                        max_out_names[0].append(name)
                                if count == 2:
                                    break
                                if count == 0:
                                    form.data[f'Day{x + 1}_1400'] = name
                                else:
                                    form.data[f'Day{x + 1}_1400'] += "\n" + name
                                count += 1
                                names_days[f'day{x}_noon'].remove(name)
                        if count < 2:
                            while count < 2:
                                self.insert_random(form, names_days[f'day{x}_noon'], "1400", x, count)
                                count += 1
                    else:
                        chosen = self.search_and_put(form, names_days[f'day{x - 1}_night'],
                                                     names_days[f'day{x}_noon'], x,
                                                     "1400", max_out_names[0], 0, sequence_count, max_seq0,
                                                     max_seq1, True, [])
                        if not chosen:
                            self.insert_random(form, names_days[f'day{x}_noon'], "1400", x, 0)
                            chosen = True
                    # noon
                    self.insert_all_to_form(form, names_days[f'day{x}_noon'], x, "1500")
                # morning
                count = 0
                if not chosen:
                    self.insert_random(form, names_days[f'day{x}_morning'], "700_search", x, 0)
                chosen = False
                for morning in range(len(names_days[f'day{x}_morning'])):
                    r = random.randint(0, len(names_days[f'day{x}_morning']) - 1)
                    if count < 3:
                        form.data[f'Day{x + 1}_720_{count + 1}'] = names_days[f'day{x}_morning'][r]
                    else:
                        form.data[f'Day{x + 1}_720_3'] += "\n" + names_days[f'day{x}_morning'][r]
                    names_days[f'day{x}_morning'].pop(r)
                    count += 1
                # night
                self.insert_all_to_form(form, names_days[f'day{x}_night'], x, "2300")
            else:
                count = 0
                shift = "_700_search"
                # morning
                for name in names_days[f'day{x}_morning']:
                    if count == 2:
                        shift = "_700_manager"
                    if count == 0 or count == 2:
                        form.data[f'Day{x + 1}{shift}'] = name
                    else:
                        form.data[f'Day{x + 1}{shift}'] += "\n" + name
                    count += 1
                # noon
                self.insert_all_to_form(form, names_days[f'day{x}_noon'], x, "1500")
                # night
                self.insert_all_to_form(form, names_days[f'day{x}_night'], x, "2300")
        form.data._mutable = False
        if form.is_valid():
            self.object = form.save()
            messages.success(self.request, f'העלאה הושלמה')
        else:
            messages.info(self.request, f'עדכון לא הושלם תקלה טכנית')


def is_more_than_once(list, name):
    num = 0
    for n in list:
        if n == name:
            num += 1
    if num > 1:
        return True
    return False


@login_required
def organization(request):
    is_empty = False
    is_couple = False
    days = {}
    days_before = {}
    all_organizations = Organization.objects.all()
    organization_last = all_organizations.order_by('-date')[0]
    if organization_last.published:
        for x in range(14):
            days["day" + str(x)] = organization_last.date + datetime.timedelta(days=x)
        organization_last_input = get_input(organization_last)
        is_couple = len(Organization.objects.all()) > 1
        if is_couple:
            organization_last = all_organizations.order_by('-date')[1]
            for x in range(14):
                days_before["day" + str(x)] = organization_last.date \
                                              + datetime.timedelta(days=x)
            organization_before_input = get_input(organization_last)
    elif len(all_organizations) > 1:
        organization_last = all_organizations.order_by('-date')[1]
        for x in range(14):
            days["day" + str(x)] = organization_last.date + datetime.timedelta(days=x)
        organization_last_input = get_input(organization_last)
        is_couple = len(Organization.objects.all()) > 2
        if is_couple:
            organization_last = all_organizations.order_by('-date')[2]
            for x in range(14):
                days_before["day" + str(x)] = organization_last.date \
                                              + datetime.timedelta(days=x)
            organization_before_input = get_input(organization_last)
    else:
        is_empty = True
    if is_empty:
        context = {
            "is_empty": is_empty
        }
    else:
        if is_couple:
            organization_last1 = {"z_630": [], "z_700_search": [], "z_700_manager": [], "z_720_1": [], "z_720_2": [],
                                  "z_720_3": [], "z_720_pull": [], "z_1400": [], "z_1500": [], "z_1500_1900": [],
                                  "z_2300": [], "z_notes": []}
            organization_last2 = {"z_630": [], "z_700_search": [], "z_700_manager": [], "z_720_1": [], "z_720_2": [],
                                  "z_720_3": [], "z_720_pull": [], "z_1400": [], "z_1500": [], "z_1500_1900": [],
                                  "z_2300": [], "z_notes": []}
            for x in range(1, 15):
                day = "day" + str(x)
                for key in organization_last1:
                    organization_last1[key].append(organization_last_input[day + key.replace("z", "")])
                    organization_last2[key].append(organization_before_input[day + key.replace("z", "")])
            context = {
                "days": days,
                "organization_input": organization_last1,
                "is_couple": is_couple,
                "organization_before_input": organization_last2,
                "days_before": days_before,
                "nickname": request.user.profile.nickname,
            }
        else:
            organization_last1 = {"z_630": [], "z_700_search": [], "z_700_manager": [], "z_720_1": [], "z_720_2": [],
                                  "z_720_3": [], "z_720_pull": [], "z_1400": [], "z_1500": [], "z_1500_1900": [],
                                  "z_2300": [], "z_notes": []}
            for x in range(1, 15):
                day = "day" + str(x)
                for key in organization_last1:
                    organization_last1[key].append(organization_last_input[day + key.replace("z", "")])
            context = {
                "days": days,
                "organization_input": organization_last1,
                "is_couple": is_couple,
                "nickname": request.user.profile.nickname,
            }
    return render(request, "Schedule/Organization.html", context)


def WriteToExcel(served, notes, dates):
    # Create a workbook and add a worksheet.
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    worksheet.right_to_left()

    days = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"]

    maxes = {"morning": 0, "after_noon": 0, "night": 0}

    for key in served:
        temp = 0
        if key.count("M"):
            split = served[key].split("\n")
            for x in range(len(split)):
                if split[x] != "(לא משיכה)":
                    temp += 1
            if temp > maxes["morning"]:
                maxes["morning"] = temp
        elif key.count("A"):
            split = served[key].split("\n")
            if len(split) > maxes["after_noon"]:
                maxes["after_noon"] = len(split)
        else:
            split = served[key].split("\n")
            if len(split) > maxes["night"]:
                maxes["night"] = len(split)

    maxes["morning"] += 1
    maxes["after_noon"] += 2
    maxes["night"] += 2

    # Write a total using a formula.
    title_format = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': 24,
        'fg_color': 'white'})
    cell_format = workbook.add_format({
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
    })
    cell_no_pull_format = workbook.add_format({
        'font_color': "#ff0000"
    })
    border_bottom_format = workbook.add_format({
        'bottom': 5,
        'bottom_color': '#000000'
    })
    border_left_format = workbook.add_format({
        'left': 5,
        'left_color': '#000000'
    })
    border_left_bottom_format = workbook.add_format({
        'left': 5,
        'left_color': '#000000',
        'bottom': 5,
        'bottom_color': '#000000',
    })
    # Building first Structure
    col = 0
    for x in range(15):
        worksheet.write(4 + maxes["morning"], col, None, border_bottom_format)
        worksheet.write(4 + maxes["after_noon"] + maxes["morning"], col, None, border_bottom_format)
        col += 1
    row = 0
    sum_maxes = maxes["morning"] + maxes["after_noon"] + maxes["night"] + 6
    for x in range(sum_maxes):
        if x == 4 + maxes["morning"] or x == 4 + maxes["morning"] + maxes["after_noon"]:
            worksheet.write(row, 8, None, border_left_bottom_format)
        else:
            worksheet.write(row, 8, None, border_left_format)
        row += 1
    # Building second Structure
    worksheet.merge_range('A1:H2', 'הגשות', title_format)
    worksheet.merge_range('I1:P2', 'הגשות', title_format)
    worksheet.merge_range('Q1:X2', dates["day0"].strftime("%d.%m") + "-" + dates["day13"].strftime("%d.%m"),
                          title_format)
    worksheet.write(2, 0, "תאריך", cell_format)
    col = 1
    for d in dates:
        worksheet.write(2, col, dates[d].strftime("%d.%m"), cell_format)
        col += 1
    worksheet.write(3, 0, "יום", cell_format)
    col = 1
    for d in days:
        worksheet.write(3, col, d, cell_format)
        worksheet.write(3, col + 7, d, cell_format)
        col += 1
    worksheet.merge_range(f'A5:A{5 + maxes["morning"]}', 'בוקר', cell_format)
    worksheet.merge_range(
        f'A{5 + maxes["morning"] + 1}:A{5 + maxes["morning"] + maxes["after_noon"]}', 'צהריים', cell_format)
    worksheet.merge_range(
        f'A{5 + maxes["morning"] + maxes["after_noon"] + 1}:A{5 + maxes["morning"] + maxes["after_noon"] + maxes["night"]}',
        'לילה', cell_format)
    worksheet.merge_range('Q4:R4', 'שם', cell_format)
    worksheet.write("S4", "בוקר 1", cell_format)
    worksheet.write("T4", "בוקר 2", cell_format)
    worksheet.write("U4", "צהריים 1", cell_format)
    worksheet.write("V4", "צהריים 2", cell_format)
    worksheet.write("W4", "לילה", cell_format)
    worksheet.write("X4", "סופ\"ש", cell_format)

    # Adding Data
    users = []
    row = 4
    col = 1
    for key in served:
        if key.count("M"):
            day = int(key.replace("M", ""))
            row = 4
            split = served[key].split("\n")
            for x in range(len(split)):
                if split[x] != "(לא משיכה)":
                    if x + 1 < len(split):
                        if split[x + 1] == "(לא משיכה)":
                            worksheet.write(row, day, split[x], cell_no_pull_format)
                        else:
                            worksheet.write(row, day, split[x])
                    else:
                        worksheet.write(row, day, split[x])
                    if split[x] not in users:
                        users.append(split[x])
                    row += 1
        elif key.count("A"):
            day = int(key.replace("A", ""))
            row = 4 + maxes["morning"] + 1
            split = served[key].split("\n")
            for x in range(len(split)):
                worksheet.write(row, day, split[x])
                if split[x] not in users:
                    users.append(split[x])
                row += 1
        else:
            day = int(key.replace("N", ""))
            row = 4 + maxes["morning"] + maxes["after_noon"] + 1
            split = served[key].split("\n")
            for x in range(len(split)):
                worksheet.write(row, day, split[x])
                if split[x] not in users:
                    users.append(split[x])
                row += 1

    num_rows = len(users) + 1
    col = 18
    for x in range(num_rows):
        col = 18
        if x == 0:
            worksheet.merge_range(f'Q{4 + x + 1}:R{4 + x + 1}', '', cell_format)
        else:
            worksheet.merge_range(f'Q{4 + x + 1}:R{4 + x + 1}', users[x - 1], cell_format)
        for c in range(6):
            worksheet.write(4 + x, col, "", cell_format)
            col += 1
    worksheet.merge_range(f'Q{4 + num_rows + 1}:R{4 + num_rows + 1}', 'סה\"כ', cell_format)
    worksheet.write(f'S{4 + num_rows + 1}', f'=SUM(S5:S{4 + num_rows})', cell_format)
    worksheet.write(f'T{4 + num_rows + 1}', f'=SUM(T5:T{4 + num_rows})', cell_format)
    worksheet.write(f'U{4 + num_rows + 1}', f'=SUM(U5:U{4 + num_rows})', cell_format)
    worksheet.write(f'V{4 + num_rows + 1}', f'=SUM(V5:V{4 + num_rows})', cell_format)
    worksheet.write(f'W{4 + num_rows + 1}', f'=SUM(W5:W{4 + num_rows})', cell_format)
    worksheet.write(f'X{4 + num_rows + 1}', f'=SUM(X5:X{4 + num_rows})', cell_format)

    row = 4 + num_rows + 4

    worksheet.merge_range(f'Q{row}:X{row + 3}', 'משמרות לאיכות', title_format)
    worksheet.merge_range(f'Q{row + 4}:X{row + 5}', 'שבוע ראשון', title_format)
    worksheet.merge_range(f'Q{row + 6}:X{row + 6}', '', cell_format)
    worksheet.merge_range(f'Q{row + 7}:X{row + 7}', '', cell_format)
    worksheet.merge_range(f'Q{row + 8}:X{row + 9}', 'שבוע שני', title_format)
    worksheet.merge_range(f'Q{row + 10}:X{row + 10}', '', cell_format)
    worksheet.merge_range(f'Q{row + 11}:X{row + 11}', '', cell_format)

    row = row + 13
    count = 0
    for n in notes:
        if n == "general":
            worksheet.merge_range(f'Q{row + count}:X{row + count + 1}', 'הערות', title_format)
            count += 2
        elif n == "week1":
            worksheet.merge_range(f'Q{row + count}:X{row + count}', 'שבוע ראשון', title_format)
            count += 1
        else:
            worksheet.merge_range(f'Q{row + count}:X{row + count}', 'שבוע שני', title_format)
            count += 1
        split = notes[n].split("\n")
        if len(split) > 0:
            for s in split:
                worksheet.merge_range(f'Q{row + count}:X{row + count}', s, cell_format)
                count += 1

    worksheet.merge_range(f'Z4:AE5', 'אירועים', title_format)
    events = Event.objects.all()
    events_notes = ""
    for x in range(14):
        if len(events.filter(date2=dates["day" + str(x)])) > 0:
            for ev in events.filter(date2=dates["day" + str(x)]):
                if ev.nickname != "כולם":
                    events_notes = events_notes + f'בתאריך {ev.date2} יש {ev.description} ל{ev.nickname}' + "\n"
                else:
                    events_notes = events_notes + f'בתאריך {ev.date2} יש {ev.description}' + "\n"
    split = events_notes.split("\n")
    row = 6
    count = 0
    for s in split:
        worksheet.merge_range(f'Z{row + count}:AE{row + count}', s, cell_format)
        count += 1

    workbook.close()
    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    file_name = "serve" + dates["day0"].strftime("%d.%m")
    return FileResponse(buffer, as_attachment=True, filename=f'{file_name}.xlsx')


def number_to_day2(num):
    day = "יום "
    if num == 1:
        return day + "ראשון"
    elif num == 2:
        return day + "שני"
    elif num == 3:
        return day + "שלישי"
    elif num == 4:
        return day + "רביעי"
    elif num == 5:
        return day + "חמישי"
    elif num == 6:
        return day + "שישי"
    else:
        return day + "שבת"


guards_num = {}
for x in range(14):
    guards_num[f"M{x}"] = 5
    guards_num[f"A{x}"] = 3
    guards_num[f"N{x}"] = 1
guards_num["A13"] = 0
guards_num["A12"] = 0
guards_num["M12"] = 0
guards_num["A6"] = 0
guards_num["M5"] = 0
guards_num["A5"] = 0
guards_num["N13"] = 2
guards_num["N12"] = 2
guards_num["M13"] = 2
guards_num["N6"] = 2
guards_num["N5"] = 2
guards_num["M6"] = 2


def compare_organizations(served, guards_num):
    organizer = Organizer(served, guards_num)
    organizer.organize()
    for i in range(1):
        new_organizer = Organizer(served, guards_num)
        new_organizer.organize()
        if organizer.notes > new_organizer.notes:
            organizer = new_organizer
        if organizer.notes == 0:
            break
    return organizer


@staff_member_required
def suggestion(request):
    served = {}
    for i in range(14):
        served["M" + str(i)] = []
        served["A" + str(i)] = []
        served["N" + str(i)] = []
    shift_date = Organization.objects.order_by('-date')[0].date
    shifts_served = Shift.objects.all().filter(date=shift_date)
    for shift in shifts_served:
        shifts = [shift.M1, shift.A1, shift.N1, shift.M2, shift.A2, shift.N2, shift.M3,
                  shift.A3, shift.N3, shift.M4, shift.A4, shift.N4, shift.M5, shift.A5, shift.N5,
                  shift.M6, shift.A6, shift.N6, shift.M7, shift.A7, shift.N7, shift.M8,
                  shift.A8, shift.N8, shift.M9, shift.A9, shift.N9, shift.M10, shift.A10,
                  shift.N10, shift.M11, shift.A11, shift.N11, shift.M12, shift.A12, shift.N12,
                  shift.M13, shift.A13, shift.N13, shift.M14, shift.A14, shift.N14]
        kind = "M"
        count = 0
        index = 0
        for s in shifts:
            if s:
                served[kind + str(index)].append(shift.username.profile.nickname)
            count = count + 1
            if count == 0:
                kind = "M"
            elif count == 1:
                kind = "A"
            elif count == 2:
                kind = "N"
            else:
                kind = "M"
                index = index + 1
                count = 0
    days = {}
    for x in range(14):
        days[f'day{x}'] = Organization.objects.order_by('-date')[0].date + datetime.timedelta(days=x)
    # organizer = Organizer(served, guards_num)
    # organizer.organize()
    organizer = compare_organizations(served, guards_num)
    if request.method == 'POST':
        for x in range(14):
            day = f'M{x}'
            if x == 6 or x == 13:
                guards_num[day] = int(request.POST.get(day, 2))
            elif x == 5 or x == 12:
                guards_num[day] = int(request.POST.get(day, 0))
            else:
                guards_num[day] = int(request.POST.get(day, 5))
            day = f'A{x}'
            if x == 5 or x == 6 or x == 12 or x == 13:
                guards_num[day] = int(request.POST.get(day, 0))
            else:
                guards_num[day] = int(request.POST.get(day, 3))
            day = f'N{x}'
            if x == 5 or x == 6 or x == 12 or x == 13:
                guards_num[day] = int(request.POST.get(day, 2))
            else:
                guards_num[day] = int(request.POST.get(day, 1))
        # organizer = Organizer(served, guards_num)
        # organizer.organize()
        organizer = compare_organizations(served, guards_num)
        context = {
            "days": days,
            "organized": organizer.organized,
            "notes": organizer.notes,
            "guardsnumbers": guards_num
        }
        return render(request, "Schedule/Suggestion.html", context)
    else:
        context = {
            "days": days,
            "organized": organizer.organized,
            "notes": organizer.notes,
            "guardsnumbers": guards_num
        }
    return render(request, "Schedule/Suggestion.html", context)


# filters


@register.filter
def get_user_name(username):
    user = User.objects.all().filter(username=username).first()
    name = user.first_name + " " + user.last_name
    return name


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def is_divided5(num):
    if num % 5 == 0:
        return True
    return False


@register.filter
def get_index(list, item):
    return list.index(item)


@register.filter
def minus(item, num):
    return item - num


@register.filter
def plus_days(date):
    return date + datetime.timedelta(days=13)


@register.filter
def cut_list(list, num):
    new_list = []
    if num == 1:
        for x in range(7):
            new_list.append(list[x])
    else:
        for x in range(7, len(list)):
            new_list.append(list[x])
    return new_list


@register.filter
def is_in_td(text, nickname):
    if text is not None and len(text) > 0:
        split = text.split("\n")
        for s in split:
            s = s.replace(" ", "")
            s = s.replace("\n", "")
            s = s.replace("\r", "")
            if nickname == s:
                return True
    return False


@register.filter
def is_string(item):
    return isinstance(item, str)

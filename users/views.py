from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from Schedule.models import Settings as Settings
from django.utils.translation import activate
from requests import get
from Schedule.models import IpBan


activate('he')


def register(request, *args, **kwargs):
    activate('he')
    settings = Settings.objects.first()
    pin_code = int(settings.pin_code)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print('My public IP address is: {}'.format(ip))
    ips = IpBan.objects.all()
    ban = False
    if len(ips.filter(ipaddress=ip)) > 0:
        new_ip = ips.filter(ipaddress=ip).first()
        if new_ip.num_tries > 15:
            ban = True
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if ban:
            return render(request, "users/register.html", {"form": form, "ban": ban})
        ips = IpBan.objects.all()
        if len(ips.filter(ipaddress=ip)) == 0:
            new_ip = IpBan(ipaddress=ip, num_tries=1)
            new_ip.save()
        else:
            new_ip = ips.filter(ipaddress=ip).first()
            new_ip.num_tries += 1
            new_ip.save()
        pc = int(request.POST.get("pin_code"))
        if pc != pin_code:
            messages.warning(request, "קוד זיהוי לא נכון")
        elif form.is_valid():
            form.save(commit=True)
            username = form.cleaned_data.get("username")
            messages.success(request, f'{username}נוצר חשבון ל ')
            return redirect("login")
        else:
            messages.warning(request, form.errors)
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form, "ban": ban})


@login_required
def profile(request):
    activate('he')
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'פרטים עודכנו')
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        "u_form": u_form,
        "p_form": p_form,
        "night": request.user.profile.night,
        "sat_night": request.user.profile.sat_night,
        "sat_morning": request.user.profile.sat_morning,
        "sat_noon": request.user.profile.sat_noon,
    }
    return render(request, "users/profile.html", context)

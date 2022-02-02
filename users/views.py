from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, AuthenticationForm
from Schedule.models import Settings3 as Settings
from django.utils.translation import activate
from .models import UserSettings as USettings
from requests import get
from Schedule.models import IpBan
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('Schedule-Home')
        else:
            messages.warning(request, "שם משתמש או סיסמא לא נכונים")
            return HttpResponseRedirect('/login')

    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

def register(request, *args, **kwargs):
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
    user_settings = USettings.objects.all().filter(user=request.user).first()
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user_settings)
        p_form.instance.language = request.POST.get("languages")
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'פרטים עודכנו')
            return redirect("profile")
        else:
            messages.warning(request, f'פרטים לא עודכנו')
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=user_settings)
    context = {
        "u_form": u_form,
        "p_form": p_form,
        "night": user_settings.night,
        "sat_night": user_settings.sat_night,
        "sat_morning": user_settings.sat_morning,
        "sat_noon": user_settings.sat_noon,
        "language": user_settings.language
    }
    return render(request, "users/profile.html", context)

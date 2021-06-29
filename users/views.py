from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from Schedule.models import Settings as Settings
from django.utils.translation import activate


activate('he')


def register(request, *args, **kwargs):
    activate('he')
    settings = Settings.objects.first()
    pin_code = int(settings.pin_code)
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
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
    return render(request, "users/register.html", {"form": form})


@login_required
def profile(request):
    activate('he')
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile2)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'פרטים עודכנו')
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile2)
    context = {
        "u_form": u_form,
        "p_form": p_form,
        "night": request.user.profile2.night,
        "sat_night": request.user.profile2.sat_night,
        "sat_morning": request.user.profile2.sat_morning,
        "sat_noon": request.user.profile2.sat_noon,
    }
    return render(request, "users/profile.html", context)

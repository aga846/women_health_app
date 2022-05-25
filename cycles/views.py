from django.shortcuts import render, get_object_or_404, redirect
from cycles.forms import CyclesLengthForm, TemperatureForm
from cycles.models import CyclesLength, Temperature
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
import datetime as dt
from django.utils import timezone
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode
# Create your views here.


def count_last_day(cycle):
    return cycle.first_day + dt.timedelta(days=cycle.length)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print(request.POST)
            username = request.POST["username"]
            password = request.POST["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            return HttpResponseRedirect(reverse("cycles:add_new_cycle",))

    else:
        form = UserCreationForm()

    context = {"form": form}
    return render(request, "cycles/register.html", context)


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            cycle_row = CyclesLength.objects.filter(user=request.user)
            if cycle_row:
                last_cycle = (CyclesLength.objects.filter(user=request.user,
                                                          first_day__lte=timezone.now()).order_by("-first_day"))[0]
                pk = last_cycle.pk
                return HttpResponseRedirect(reverse("cycles:about", args=(pk,)))
            else:
                return HttpResponseRedirect(reverse("cycles:add_new_cycle",))

        else:
            raise Http404
    else:
        return render(request, "cycles/login.html")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index",))


def index(request):
    if request.method == "POST":
        form = CyclesLengthForm(request.POST)
        if form.is_valid():
            length = form.cleaned_data["length"]
            first_day = form.cleaned_data["first_day"]

            query_string = urlencode(
                {"length": length, "first_day": first_day})

            if request.POST["action"] == "I want to have a baby":
                base_url = reverse("cycles:baby")
                url = f"{base_url}?{query_string}"
                return redirect(url)
            else:
                base_url = reverse("cycles:no_baby")
                url = f"{base_url}?{query_string}"
                return redirect(url)
        else:
            return render(request, "cycles/index.html", {"form": CyclesLengthForm(request.POST)})
    else:
        if request.user.is_authenticated:
            last_cycle = (CyclesLength.objects.filter(user=request.user,
                                                      first_day__lte=timezone.now()).order_by("-first_day"))[0]
            pk = last_cycle.pk
            return redirect("cycles:about", pk=pk)
        else:
            return render(request, "cycles/index.html", {"form": CyclesLengthForm()})


@login_required
def add_new_cycle(request):
    if request.method == "POST":
        form = CyclesLengthForm(request.POST)
        if form.is_valid():
            length = form.cleaned_data["length"]
            first_day = form.cleaned_data["first_day"]
            cycle = form.save(commit=False)
            cycle.user = request.user
            cycle.save()
            pk = cycle.pk
            return HttpResponseRedirect(reverse("cycles:about", args=(pk,)))
        else:
            return render(request, "cycles/add_new_cycle.html", {"form": CyclesLengthForm(request.POST)})
    else:
        return render(request, "cycles/add_new_cycle.html", {"form": CyclesLengthForm()})


def baby(request):
    length = int(request.GET.get("length"))
    first_day = dt.datetime.strptime(request.GET.get("first_day"), "%Y-%m-%d")
    last_day = first_day + dt.timedelta(days=length)
    ovulation_day = last_day - dt.timedelta(days=14)
    first_fertile = ovulation_day - dt.timedelta(days=3)
    day_after = ovulation_day + dt.timedelta(days=1)
    best_days = {"ovulation_day": ovulation_day,
                 "first_fertile": first_fertile, "day_after": day_after}
    return render(request, "cycles/baby.html", context=best_days)


def no_baby(request):
    length = int(request.GET.get("length"))
    first_day = dt.datetime.strptime(request.GET.get("first_day"), "%Y-%m-%d")
    last_day = first_day + dt.timedelta(days=length)
    ovulation_day = last_day - dt.timedelta(days=14)
    last_day_before = ovulation_day - dt.timedelta(days=4)
    first_day_after = ovulation_day + dt.timedelta(days=3)
    safe_days = {"first_day": first_day, "last_day_before": last_day_before,
                 "first_day_after": first_day_after, "last_day": last_day}
    return render(request, "cycles/no_baby.html", context=safe_days)


@login_required
def about(request, pk):
    cycle = (CyclesLength.objects.get(user=request.user, pk=pk))
    is_last_cycle = ""
    if cycle.pk == ((CyclesLength.objects.filter(user=request.user,
                    first_day__lte=timezone.now()).order_by("-first_day"))[0]).pk:
        is_last_cycle = True

    first_day = cycle.first_day
    last_day = first_day + dt.timedelta(days=cycle.length)
    ovulation_day = last_day - dt.timedelta(days=14)

    # Want to have a baby
    first_fertile = ovulation_day - dt.timedelta(days=3)
    day_after = ovulation_day + dt.timedelta(days=1)

    # Want to avoid pregnacy
    last_day_before = ovulation_day - dt.timedelta(days=4)
    first_day_after = ovulation_day + dt.timedelta(days=3)

    days = {"ovulation_day": ovulation_day,
            "first_fertile": first_fertile, "day_after": day_after,
            "first_day": first_day, "last_day_before": last_day_before,
            "first_day_after": first_day_after, "last_day": last_day,
            "user": request.user, "is_last_cycle": is_last_cycle,
            "pk": cycle.pk}

    return render(request, "cycles/about.html", context=days)


@login_required
def temperatures(request, pk):
    cycle = CyclesLength.objects.get(pk=pk)
    temperatures = Temperature.objects.filter(
        cycle=cycle).order_by("day_of_cycle")

    #checking when the ovulation was
    temps = [temperature.temperature for temperature in temperatures]
    difference = 0.2
    colors = ["day" for temp in temps]

    if len(temps) >= 4:
        for index, temp in enumerate(temps[3:], start=3):
            base_value = temps[index-3] + difference
            print(index, temp)
            if (temp >= base_value) and (temps[index-1] >= base_value) and (temps[index-2] >= base_value):
                colors[index-3] = "ovulation_day"
                print(f"ovulation on {index-2} day")
                break

    temperatures_colors = list(zip(temperatures, colors))

    is_last_cycle = ""
    if cycle.pk == ((CyclesLength.objects.filter(user=request.user,
                    first_day__lte=timezone.now()).order_by("-first_day"))[0]).pk:
        is_last_cycle = True

    first_day = cycle.first_day
    last_day = first_day + dt.timedelta(days=cycle.length)
    context = {"pk": pk, "user": request.user, "temperatures_colors": temperatures_colors,
               "first_day": first_day, "last_day": last_day, "is_last_cycle": is_last_cycle,
               }
    return render(request, "cycles/temperatures.html", context=context)


@login_required
def add_temperature(request, pk):
    if request.method == "POST":
        form = TemperatureForm(request.POST)
        if form.is_valid():
            day_of_cycle = form.cleaned_data["day_of_cycle"]
            temperature = form.cleaned_data["temperature"]
            temperature = form.save(commit=False)
            temperature.cycle = CyclesLength.objects.get(pk=pk)
            temperature.save()
            return HttpResponseRedirect(reverse("cycles:temperatures", args=(pk,)))
        else:
            return render(request, "cycles/add_temperature.html", {"form": TemperatureForm(request.POST)})
    else:
        return render(request, "cycles/add_temperature.html", {"form": TemperatureForm(), "pk": pk})


@login_required
def cycles_list(request, user):
    cycles_list = CyclesLength.objects.filter(
        user=request.user).order_by("-first_day")
    cycles = [cycle for cycle in cycles_list]
    last_days = [count_last_day(cycle) for cycle in cycles_list]
    lengths = [cycle.length for cycle in cycles_list]
    cycles_dates = list(zip(cycles, last_days, lengths))
    return render(request, "cycles/cycles_list.html", {"cycles_dates": cycles_dates})


@login_required
def confirm_delete(request, pk):
    cycle = (CyclesLength.objects.get(user=request.user, pk=pk))
    first_day = cycle.first_day
    last_day = first_day + dt.timedelta(days=cycle.length)
    return render(request, "cycles/confirm_delete.html",
                  {"first_day": first_day, "last_day": last_day,
                   "user": request.user, "pk": pk})


@login_required
def delete_cycle(request, pk):
    cycle = get_object_or_404(CyclesLength, pk=pk)
    cycle.delete()
    return redirect("cycles:cycles_list", user=request.user)


@login_required
def update_cycle(request, pk):
    if request.method == "POST":
        form = CyclesLengthForm(request.POST)
        if form.is_valid():
            length = form.cleaned_data["length"]
            first_day = form.cleaned_data["first_day"]
            old_cycle = CyclesLength.objects.filter(user=request.user, pk=pk)
            old_cycle.update(length=length, first_day=first_day)
            user = request.user
            return HttpResponseRedirect(reverse("cycles:cycles_list", args=(user,)))

        else:
            return render(request, "cycles/update_cycle.html", {"form": CyclesLengthForm(request.POST)})
    else:
        return render(request, "cycles/update_cycle.html", {"form": CyclesLengthForm(), "pk": pk, "user": request.user})

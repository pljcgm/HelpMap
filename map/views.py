from django.shortcuts import render, redirect
from django.contrib import messages
from opencage.geocoder import OpenCageGeocode
from map.forms import *
from map.models import *
from map.config.keys import OPENCAGE_API_KEY


def index(request):
    context = {"page_title": "Map"}
    help_points = HelpPoint.objects.all()
    context["help_points"] = help_points
    return render(request, "map/map.html", context)


def new_help_point(request):
    if request.user.is_authenticated:
        context = {"page_title": "Offer Help"}
        if request.method == "POST":
            form = NewHelpPointForm(request.POST)
            if form.is_valid():
                try:
                    street_and_nr = form.cleaned_data.get("street")
                    zip_and_city = form.cleaned_data.get("zip_and_city")
                    title = form.cleaned_data.get("title")
                    description = form.cleaned_data.get("description")
                    category = Category.objects.all().filter(title=form.cleaned_data.get("category"))[0]
                    point = get_lat_long(street_and_nr, zip_and_city)
                    map_point = {
                        'type': 'Point',
                        'coordinates': point
                    }

                    new_point = HelpPoint(author=request.user, title=title, description=description, geom=map_point,
                                          category=category)
                    new_point.save()
                    context["form"] = form
                    context["saved_point"] = new_point
                    messages.add_message(request, messages.SUCCESS, "Your point has been added!")
                    return render(request, "map/add_help_point.html", context)

                except Exception as e:
                    messages.add_message(request, messages.ERROR, e)
                    context["form"] = form
            else:
                messages.add_message(request, messages.ERROR, "Form is invalid!")
                context["form"] = form
        else:
            form = NewHelpPointForm()
            context["form"] = form
            return render(request, "map/add_help_point.html", context)
        return render(request, "map/add_help_point.html", context)
    else:
        messages.add_message(request, messages.ERROR, "You have to be logged in to do that!")
        return redirect("login")


def get_info(request):
    context = {"page_title": "Info"}
    return render(request, "info.html", context)


def get_lat_long(street_and_nr, zip_and_city):
    geocoder = OpenCageGeocode(OPENCAGE_API_KEY)
    query = ", ".join([street_and_nr, zip_and_city])
    results = geocoder.geocode(query)[0]['geometry']
    return [results['lng'], results['lat']]
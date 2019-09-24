from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from .models import shows
from django.utils.dateparse import parse_date
# line added during the implementation of validation .
from django.contrib import messages


def index(request):
    print("Redirecting home to all shows page...")
    return redirect("/shows")


def new(request):
    if request.method == "GET":
        return render(request, "tv_shows_app/create.html")


def create(request):

    if request.method == "POST":
        # Pass the post data to the mehod we wrote and save the response in a variable called errors
        errors = shows.objects.basic_validator(request.POST)
        
        # check if the errors dictionary has anything in it
        if len(errors) > 0:
            # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
            for key, value in errors.items():
                print(value)
                messages.error(request, value)
            return redirect("/shows/new")

        else:
            # if the errors object is empty = no errors = then we can proceed to save the data.
            new_show = shows.objects.create(title=request.POST['title'],
                                            network=request.POST['network'],
                                            release_date=parse_date(request.POST['release_date']),
                                            desc=request.POST['desc'])
            newshow = "/shows/" + str(new_show.id)
            print(newshow)
            return redirect(newshow)


def display_all(request):
    if request.method == "GET":
        allshows = shows.objects.all()
        context = {
            "all_shows": allshows
        }
        return render(request, "tv_shows_app/shows.html", context)


def display_one(request, show_id):
    if request.method == "GET":
        show = shows.objects.get(id=show_id)
        context = {
            "show": show
        }
        return render(request, "tv_shows_app/show.html", context)


def edit(request, show_id):
    if request.method == "GET":
        show = shows.objects.get(id=show_id)
        print(show.release_date)
        rel_date = show.release_date.strftime("%Y-%m-%d")
        context = {
            "show": show,
            "release_date": rel_date
        }
        return render(request, "tv_shows_app/edit.html", context)


def update(request, show_id):

    if request.method == "POST":
        errors = shows.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                print(value)
                messages.error(request, value)
            return redirect(f"/shows/{str(show_id)}/edit")
        else:
            update_show = shows.objects.get(id=show_id)
            update_show.title = request.POST['title']
            update_show.network = request.POST['network']
            update_show.release_date = parse_date(request.POST['release_date'])
            update_show.desc = request.POST['desc']
            update_show.save()
            newshow = "/shows/" + str(show_id)
            print(newshow)
            return redirect(newshow)

def destroy(request, show_id):
    d = shows.objects.get(id=show_id)
    print(f"----- Deleting Record: {str(show_id)} -{d.title}")
    d.delete()
    return redirect("/shows")

from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
import markdown2
import random as rmd


from . import util


class NewTaskForm(forms.Form):
    title = forms.CharField(label="Title")
    entry_description = forms.CharField(widget=forms.Textarea)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def content(request, entry):
    content = util.get_entry(entry)
    if content == None:
        entry = None
    else:
        content = markdown2.markdown(content)

    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "content": content
    })


def random(request):
    entries = util.list_entries()
    random_entry = rmd.choice(entries)
    return HttpResponseRedirect(reverse("wiki:content", args=[random_entry]))


def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            existing_entries = util.list_entries()
            title = form.cleaned_data["title"]
            description = form.cleaned_data["entry_description"]
            # checks if an entry with that title already exists
            if (title in existing_entries):
                return HttpResponse("An entry with that title already exists")
            else:
                new_entry = util.save_entry(title, description)
                return HttpResponseRedirect(reverse("wiki:content", args=[title]))
    return render(request, "encyclopedia/add.html", {
        "form": NewTaskForm()
    })


def edit(request, entry):
    content = util.get_entry(entry)
    form = NewTaskForm()
    # pre-populates fields
    form["title"].initial = entry
    form["entry_description"].initial = content
    return render(request, "encyclopedia/edit.html", {
        "form": form
    })


def update(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["entry_description"]
            new_entry = util.save_entry(title, description)
            return HttpResponseRedirect(reverse("wiki:content", args=[title]))


def search(request):
    q = request.GET.get('q')
    existing_entries = util.list_entries()
    # checks if search has an exact match
    if (q in existing_entries):
        return HttpResponseRedirect(reverse("wiki:content", args=[q]))
    # otherwise looks for substrings of the search
    else:
        matches = [i for i in existing_entries if q in i]
        return render(request, "encyclopedia/search.html", {
            "matches": matches
        })

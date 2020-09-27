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
    print("test")
    entriess = util.list_entries()
    print(type(entriess))
    random_entry = rmd.choice(entriess)
    # return content(request, random_entry)
    return HttpResponseRedirect(reverse("wiki:content", args=[random_entry]))
    # return render(request, "encyclopedia/entry.html", {
    #     "entry": random_entry,
    #     "content": markdown2.markdown(util.get_entry(random_entry))
    # })
# return HttpResponseRedirect(reverse("encyclopedia/random_entry.html"))
# return redirect('encyclopedia:wiki_page', page_title=random_entry)


def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            existing_entries = util.list_entries()
            title = form.cleaned_data["title"]
            description = form.cleaned_data["entry_description"]
            if (title in existing_entries):
                return HttpResponse("An entry with that title already exists")
            else:
                new_entry = util.save_entry(title, description)
                return HttpResponseRedirect(reverse("wiki:content", args=[title]))
    return render(request, "encyclopedia/add.html", {
        "form": NewTaskForm()
    })

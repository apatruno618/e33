from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import markdown2
import random as rmd


from . import util


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
    return HttpResponseRedirect(reverse("content", args=[random_entry]))
    # return render(request, "encyclopedia/entry.html", {
    #     "entry": random_entry,
    #     "content": markdown2.markdown(util.get_entry(random_entry))
    # })
# return HttpResponseRedirect(reverse("encyclopedia/random_entry.html"))
# return redirect('encyclopedia:wiki_page', page_title=random_entry)

from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def content(request, entry):
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "content": util.get_entry(entry)
    })

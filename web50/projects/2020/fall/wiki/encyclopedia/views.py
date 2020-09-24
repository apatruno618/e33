from django.shortcuts import render
import markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def content(request, entry):
    # content = util.get_entry(entry)
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "content": markdown2.markdown(util.get_entry(entry))
    })

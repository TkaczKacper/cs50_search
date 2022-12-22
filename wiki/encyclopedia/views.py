from django.shortcuts import render, HttpResponseRedirect, reverse
from django import forms

from . import util
import re
import markdown2
import random

entry_list = []
for entry in util.list_entries():
    entry_list.append(entry.lower())

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea)

def index(request):
    if request.method == "POST":
        name = request.POST.get('q').lower()

        entry_list_like_q = [entry.capitalize() for entry in entry_list if name in entry]
        
        if name in entry_list:
            return render(request, "encyclopedia/entry.html", {
                "title": name.capitalize(),
                "content": markdown2.markdown(util.get_entry(name)),
                "random_page": random_page()
            })

        return render(request, "encyclopedia/index.html", {
            "entries": entry_list_like_q,
            "random_page": random_page()
        })

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "random_page": random_page()
    })

def entry(request, name):
    if request.method == "POST":
        url = reverse('wiki:edit_page', kwargs={'name': name})
        return HttpResponseRedirect(url)
    return render(request, "encyclopedia/entry.html", {
        "title": name.capitalize(),
        "content": markdown2.markdown(util.get_entry(name)),
        "random_page": random_page()
    })

def edit_page(request, name):
    edit_form = NewPageForm()
    title = edit_form.fields["title"].initial = name
    content = edit_form.fields["content"].initial = util.get_entry(name)
    if request.method == "POST":
        form = NewPageForm(request.POST)
        content_updated = request.POST.get('content')
        if len(content_updated) < 10:
            print(len(content_updated))
            return render(request, 'encyclopedia/edit_page.html', {
                "edit_form": form,
                "error_message": "Content is too short",
                "title": title,
                "random_page": random_page()
            })
        util.save_entry(title, content_updated)
        url = reverse('wiki:entry', kwargs={'name': name})
        return HttpResponseRedirect(url)
    return render(request, "encyclopedia/edit_page.html", {
        "edit_form": edit_form,
        "title": title,
        "random_page": random_page()
    })

def add_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            if title.lower() not in entry_list:
                content = form.cleaned_data["content"]  
                util.save_entry(title, content)
                return render(request, "encyclopedia/add_page.html", {
                    "form": NewPageForm(),
                    "success_message": "Page added d-_-b",
                    "random_page": random_page()
                })
            else: 
                return render(request, "encyclopedia/add_page.html", {
                    "form": form,
                    "error_message": "Page with this title already exists.",
                    "random_page": random_page()
                })
    return render(request, "encyclopedia/add_page.html", {
        "form": NewPageForm(),
        "random_page": random_page()
    })


def random_page():
    return entry_list[random.randint(0, len(entry_list)-1)]
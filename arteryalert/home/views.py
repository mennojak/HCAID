from django.shortcuts import render
from django.http import HttpResponse
from .components import modelrunner


def index(request):
    	return render(request, "index.html")

def goodapp(request):
    context = {
        "result": "",
        "error": "",
    }

    if request.method == "POST":
        user_input = request.POST
        if user_input:
            context['result'] = modelrunner.predict(request.POST)
            return render(request, "goodapp/result.html", context)
        else:
            context["error"] = "Fill in all the fields (correctly)"

    return render(request, "goodapp/inputform.html", context)

def badapp(request):
    context = {
        "result": "",
        "error": "",
    }

    if request.method == "POST":
        user_input = request.POST
        if user_input:
            context['result'] = modelrunner.predict(request.POST)
            return render(request, "badapp/result.html", context)
        else:
            context["error"] = "Fill in all the fields (correctly)"

    return render(request, "badapp/inputform.html", context)
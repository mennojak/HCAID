from django.shortcuts import render
from django.http import HttpResponse
from .components import modelrunner


def index(request):
    context = {
        "result": "",
        "error": "",
    }

    if request.method == "POST":
        user_input = request.POST
        if user_input:
            context['result'] = modelrunner.predict(request.POST)
            return render(request, "result.html", context)
        else:
            context["error"] = "Fill in all the fields (correctly)"

    return render(request, "index.html", context)
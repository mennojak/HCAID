from django.shortcuts import render
from django.http import HttpResponse
from .components import modelrunner
import json


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
            # Convert request.POST to a dictionary
            user_input_dict = {key: value for key, value in user_input.items()}
            
            # Convert the dictionary to a JSON string
            user_data = json.dumps(user_input_dict)
            
            # Call the predict function with the JSON string
            context['result'] = modelrunner.predict(user_data)
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
            # Convert request.POST to a dictionary
            user_input_dict = {key: value for key, value in user_input.items()}
            
            # Convert the dictionary to a JSON string
            user_data = json.dumps(user_input_dict)
            
            # Call the predict function with the JSON string
            context['result'] = modelrunner.predict(user_data)
            return render(request, "badapp/result.html", context)
        else:
            context["error"] = "Fill in all the fields (correctly)"

    return render(request, "badapp/inputform.html", context)
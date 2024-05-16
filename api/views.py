from django.http import HttpResponse


def test(request, name=""):
    text = "Hello! " + name
    if request.GET.get("second_name"):
        text = "Hello! " + name + " " + request.GET.get("second_name")

    return HttpResponse(text)

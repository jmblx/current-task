import http

import django.http


def home(request):
    return django.http.HttpResponse("Главная")


def coffee(request):
    response = django.http.HttpResponse("Я чайник")
    response.status_code = http.HTTPStatus.IM_A_TEAPOT
    return response

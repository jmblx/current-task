import django.http


def item_list(request):
    return django.http.HttpResponse("Список элементов")


def item_detail(request, pk):
    return django.http.HttpResponse("Подробно элемент")


def item_num(request, pk):
    return django.http.HttpResponse(pk)

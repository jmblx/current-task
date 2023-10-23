from django.urls import path, re_path, register_converter

from catalog import converter, views

app_name = "catalog"

register_converter(converter.PositiveIntegerConverter, "positive")

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("<int:pk>/", views.item_detail, name="item_detail"),
    path("converter/<positive:pk>/", views.item_num, name="item_converter"),
    re_path(r"^re/(?P<pk>[1-9]\d*)/$", views.item_num, name="item_re"),
]

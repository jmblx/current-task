import django.contrib.admin

import catalog.models


django.contrib.admin.site.register(catalog.models.Category)


@django.contrib.admin.register(catalog.models.Item)
class ItemAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        catalog.models.Item.name.field.name,
        catalog.models.Item.is_published.field.name,
    )

    fields = (
        catalog.models.Item.is_published.field.name,
        catalog.models.Item.name.field.name,
        catalog.models.Item.category.field.name,
        catalog.models.Item.tags.field.name,
        catalog.models.Item.text.field.name,
    )

    list_editable = (catalog.models.Item.is_published.field.name,)
    list_display_links = (catalog.models.Item.name.field.name,)
    filter_horizontal = (catalog.models.Item.tags.field.name,)


django.contrib.admin.site.register(catalog.models.Tag)

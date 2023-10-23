import django.db.models


class AbstractModel(django.db.models.Model):
    id = django.db.models.AutoField(
        primary_key=True,
    )
    is_published = django.db.models.BooleanField(
        verbose_name="опубликовано", default=True
    )
    name = django.db.models.CharField(
        verbose_name="название",
        max_length=150,
        help_text="Максимальная длина - 150",
        unique=True,
    )
    

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

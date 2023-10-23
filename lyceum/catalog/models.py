import django.core.exceptions
import django.core.validators
import django.db.models
import django.utils.text
from django.utils.text import slugify
from transliterate import translit

import catalog.validators
import core.models


class Tag(core.models.AbstractModel):
    slug = django.db.models.SlugField(
        verbose_name="слаг",
        max_length=200,
        validators=[
            django.core.validators.validate_slug,
        ],
        unique=True,
        help_text="состоит из набора маленьких латинских букв, цифр,"
        "символов подчеркивания и дефиса",
    )
    normalized_name = django.db.models.CharField(
        max_length=255,
        editable=False,
    )

    def _normalize_name(self, name):
        transliterated_name = translit(name, "ru", reversed=True)
        normalized_name = slugify(transliterated_name)
        return slugify(normalized_name.lower())

    def save(self, *args, **kwargs):
        if not self.normalized_name:
            self.normalized_name = self._normalize_name(self.name)
        if (
            Category.objects.filter(normalized_name=self.normalized_name)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                "Категория с таким именем уже существует",
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "тег"
        verbose_name_plural = "теги"


class Category(core.models.AbstractModel):
    slug = django.db.models.SlugField(
        verbose_name="слаг",
        max_length=200,
        validators=[
            django.core.validators.validate_slug,
        ],
        unique=True,
        help_text="состоит из набора маленьких латинских букв, цифр,"
        "символов подчеркивания и дефиса",
    )
    weight = django.db.models.PositiveSmallIntegerField(
        verbose_name="вес",
        default=100,
        help_text="Минимальный вес - 1\nМаксимальный - 32767",
        validators=[
            django.core.validators.MaxValueValidator(32767),
            django.core.validators.MinValueValidator(1),
        ],
    )
    normalized_name = django.db.models.CharField(
        max_length=255,
        editable=False,
    )

    def _normalize_name(self, name):
        transliterated_name = translit(name, "ru", reversed=True)
        normalized_name = slugify(transliterated_name)
        return slugify(normalized_name.lower())

    def save(self, *args, **kwargs):
        if not self.normalized_name:
            self.normalized_name = self._normalize_name(self.name)
        if (
            Category.objects.filter(normalized_name=self.normalized_name)
            .exclude(pk=self.pk)
            .exists()
        ):
            raise django.core.exceptions.ValidationError(
                "Категория с таким именем уже существует",
            )
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Item(core.models.AbstractModel):
    text = django.db.models.TextField(
        verbose_name="текст",
        validators=[
            catalog.validators.ValidateMustContain("превосходно", "роскошно"),
        ],
        help_text="Введите текст",
    )
    category = django.db.models.ForeignKey(
        Category,
        verbose_name="категория",
        on_delete=django.db.models.deletion.CASCADE,
        help_text="Категория товара",
    )
    tags = django.db.models.ManyToManyField(
        Tag, verbose_name="тэги", help_text="Тэги товара",
    )
    main_image = django.db.models.ImageField(
        upload_to="catalog/images/",
    )

    def image_tmb(self):
        if self.main_image:

    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"

class main_image(django.db.models):
    image = django.db.models.ImageField(
        upload_to="catalog/images/",
    )

class images(django.db.models):
    

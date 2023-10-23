import http

import django.core.exceptions
import django.http
import django.test
import parameterized

import catalog.models


negative_testcases = [
            ("ДрУг*:ooоЕи-_-м'я!.я", "drugoooei-_-mjaja"),
            ("СтрaNnoe_imя", "strannoe_imja"),
        ]

positive_testcases = [
            ("Тупа_шВAB-1.*RA", "tupa_shvab-1ra"),
            ("СтрaNnoe_imя", "strannoe_imja"),
        ]


def get_content_and_status_code(root):
    response = django.test.Client().get(root)
    status_code = response.status_code
    if status_code == http.HTTPStatus.OK:
        content = response.content.decode()
    else:
        content = None
    return content, status_code


class TestCatalog(django.test.TestCase):
    def test_item_list_endpoint(self):
        content, status_code = get_content_and_status_code("/catalog/")
        self.assertEqual(status_code, http.HTTPStatus.OK)
        self.assertEqual(content, "Список элементов")

    @parameterized.parameterized.expand(
        [
            (1, http.HTTPStatus.OK),
            (0, http.HTTPStatus.OK),
            ("010", http.HTTPStatus.OK),
            ("01", http.HTTPStatus.OK),
            (10, http.HTTPStatus.OK),
            (-0, http.HTTPStatus.OK),
            (0.1, http.HTTPStatus.NOT_FOUND),
            (-1, http.HTTPStatus.NOT_FOUND),
            ("a10a", http.HTTPStatus.NOT_FOUND),
            ("a10", http.HTTPStatus.NOT_FOUND),
            ("10a", http.HTTPStatus.NOT_FOUND),
            ("1a0", http.HTTPStatus.NOT_FOUND),
            ("@$%^*", http.HTTPStatus.NOT_FOUND),
        ],
    )
    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_item_detail_endpoint(self, pk, expected_status_code):
        content, status_code = get_content_and_status_code(f"/catalog/{pk}/")
        self.assertEqual(status_code, expected_status_code)
        if status_code == http.HTTPStatus.OK:
            self.assertEqual(content, "Подробно элемент")

    @parameterized.parameterized.expand(
        [
            (1, http.HTTPStatus.OK),
            (0, http.HTTPStatus.NOT_FOUND),
            ("010", http.HTTPStatus.NOT_FOUND),
            ("01", http.HTTPStatus.NOT_FOUND),
            (10, http.HTTPStatus.OK),
            (-0, http.HTTPStatus.NOT_FOUND),
            (0.1, http.HTTPStatus.NOT_FOUND),
            (-1, http.HTTPStatus.NOT_FOUND),
            ("a10a", http.HTTPStatus.NOT_FOUND),
            ("a10", http.HTTPStatus.NOT_FOUND),
            ("10a", http.HTTPStatus.NOT_FOUND),
            ("1a0", http.HTTPStatus.NOT_FOUND),
            ("@$%^*", http.HTTPStatus.NOT_FOUND),
        ],
    )
    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_item_re_endpoint(self, pk, expected_status_code):
        content, status_code = get_content_and_status_code(
            f"/catalog/re/{pk}/",
        )
        self.assertEqual(status_code, expected_status_code)
        if status_code == http.HTTPStatus.OK:
            self.assertEqual(int(content), pk, f"got {content} expected {pk}")

    @parameterized.parameterized.expand(
        [
            (1, http.HTTPStatus.OK),
            (0, http.HTTPStatus.NOT_FOUND),
            ("010", http.HTTPStatus.NOT_FOUND),
            ("01", http.HTTPStatus.NOT_FOUND),
            (10, http.HTTPStatus.OK),
            (-0, http.HTTPStatus.NOT_FOUND),
            (0.1, http.HTTPStatus.NOT_FOUND),
            (-1, http.HTTPStatus.NOT_FOUND),
            ("a10a", http.HTTPStatus.NOT_FOUND),
            ("a10", http.HTTPStatus.NOT_FOUND),
            ("10a", http.HTTPStatus.NOT_FOUND),
            ("1a0", http.HTTPStatus.NOT_FOUND),
            ("@$%^*", http.HTTPStatus.NOT_FOUND),
        ],
    )
    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_positive_converter_endpoint(self, pk, expected_status_code):
        content, status_code = get_content_and_status_code(
            f"/catalog/converter/{pk}/",
        )
        self.assertEqual(status_code, expected_status_code)
        if status_code == http.HTTPStatus.OK:
            self.assertEqual(int(content), pk, f"got {content} expected {pk}")


class TestItem(django.test.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.category = catalog.models.Category.objects.create(
            name="Тестовая категория",
            is_published=True,
            slug="test-cat-slug",
            weight=100,
        )
        cls.tag = catalog.models.Tag.objects.create(
            name="Тестовый тэг",
            is_published=True,
            slug="test-tag-slug",
        )

    @parameterized.parameterized.expand(
        [
            (20, "Имя", "Непревосходно"),
            (21, "Имя", "Нероскошно"),
        ],
    )
    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_catalog_model_item_exception_validate(self, id, name, text):
        item_count = catalog.models.Item.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.item = catalog.models.Item(
                id=id,
                name=name,
                is_published=True,
                text=text,
                category=TestItem.category,
            )
            self.item.full_clean()
            self.tag.full_clean()
            self.tag.save()
            self.item.tags.add(self.tag)
            self.item.save()

        self.assertEqual(catalog.models.Item.objects.count(), item_count)

    @parameterized.parameterized.expand(
        [
            (21, "Имя2", "роскошно"),
            (22, "Имя3", "превосходно"),
            (22, "Имя3", "очень Роскошно"),
        ],
    )
    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_catalog_model_item_required_words(self, id, name, text):
        item_count = catalog.models.Item.objects.count()
        self.item = catalog.models.Item(
            id=id,
            name=name,
            is_published=True,
            text=text,
            category=TestItem.category,
        )
        self.item.full_clean()
        self.tag.full_clean()
        self.tag.save()
        self.item.tags.add(self.tag)
        self.item.save()

        self.assertEqual(catalog.models.Item.objects.count(), item_count + 1)


class TestCategory(django.test.TestCase):
    @parameterized.parameterized.expand(
        [
            (0,),
            (-1,),
            (32768,),
        ],
    )
    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_catalog_category_weight_negative(self, weight):
        category_count = catalog.models.Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.category = catalog.models.Category(
                id=22,
                name="Имя",
                is_published=True,
                slug="slug",
                weight=weight,
            )
            self.category.full_clean()
            self.category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(), category_count,
        )

    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_catalog_model_category_validate_negative_same_slug(self):
        category_count = catalog.models.Category.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.category = catalog.models.Category(
                id=20, name="name", is_published=True, slug="slug", weight=100,
            )
            self.category.full_clean()
            self.category.save()
            self.other_category = catalog.models.Category(
                id=21,
                name="other name",
                is_published=True,
                slug="slug",
                weight=150,
            )
            self.other_category.full_clean()
            self.other_category.save()

        self.assertEqual(
            catalog.models.Category.objects.count(), category_count + 1,
        )

    @parameterized.parameterized.expand(positive_testcases)
    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_catalog_model_category_normalized_validate_positive(
        self, name, expected,
    ):
        category_count = catalog.models.Category.objects.count()
        self.category = catalog.models.Category(
            id=20, name=name, is_published=True, slug="slug", weight=150,
        )
        self.category.full_clean()
        self.category.save()

        self.assertEqual(self.category.normalized_name, expected)
        self.assertEqual(
            catalog.models.Category.objects.count(), category_count + 1,
        )

    @parameterized.parameterized.expand(negative_testcases)
    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_catalog_model_category_normalized_validate_negative(
        self, name, name2,
    ):
        with self.assertRaises(django.core.exceptions.ValidationError):
            category_count = catalog.models.Category.objects.count()
            self.category = catalog.models.Category(
                id=20,
                name=name,
                is_published=True,
                slug="slug",
            )
            self.category.full_clean()
            self.category.save()
            self.category = catalog.models.Category(
                id=21,
                name=name,
                is_published=True,
                slug="slug2",
            )
            self.category.full_clean()
            self.category.save()
            self.assertEqual(name, name2)
            self.assertEqual(
                catalog.models.Category.objects.count(), category_count + 1,
            )


class TestTags(django.test.TestCase):
    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_catalog_model_tag_validate_negative_same_slug(self):
        tag_count = catalog.models.Tag.objects.count()
        with self.assertRaises(django.core.exceptions.ValidationError):
            self.tag = catalog.models.Tag(
                id=20,
                name="name",
                is_published=True,
                slug="slug",
            )
            self.tag.full_clean()
            self.tag.save()
            self.other_tag = catalog.models.Tag(
                id=21,
                name="other name",
                is_published=True,
                slug="slug",
            )
            self.other_tag.full_clean()
            self.other_tag.save()

        self.assertEqual(catalog.models.Tag.objects.count(), tag_count + 1)

    @parameterized.parameterized.expand(positive_testcases)
    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_catalog_model_tag_normalized_validate_positive(
        self, name, expected,
    ):
        tag_count = catalog.models.Tag.objects.count()
        self.tag = catalog.models.Tag(
            id=20,
            name=name,
            is_published=True,
            slug="slug",
        )
        self.tag.full_clean()
        self.tag.save()

        self.assertEqual(self.tag.normalized_name, expected)
        self.assertEqual(catalog.models.Tag.objects.count(), tag_count + 1)

    @parameterized.parameterized.expand(negative_testcases)
    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_catalog_model_tag_normalized_validate_negative(
        self, name, name2,
    ):
        with self.assertRaises(django.core.exceptions.ValidationError):
            tag_count = catalog.models.Tag.objects.count()
            self.tag = catalog.models.Tag(
                id=20,
                name=name,
                is_published=True,
                slug="slug",
            )
            self.tag.full_clean()
            self.tag.save()
            self.tag = catalog.models.Tag(
                id=21,
                name=name,
                is_published=True,
                slug="slug2",
            )
            self.tag.full_clean()
            self.tag.save()
            self.assertEqual(name, name2)
            self.assertEqual(catalog.models.Tag.objects.count(), tag_count + 1)

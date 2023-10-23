import http

import django.test


class TestHomepage(django.test.TestCase):
    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_homepage_endpoint(self):
        response = django.test.Client().get("")
        text = response.content.decode()
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(text, "Главная")

    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_coffee_endpoint(self):
        response = django.test.Client().get("/coffee/")
        text = response.content.decode()
        self.assertEqual(
            http.HTTPStatus.IM_A_TEAPOT,
            response.status_code,
        )
        self.assertEqual(text, "Я чайник")

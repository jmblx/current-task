import http

import django.test


class TestAbout(django.test.TestCase):
    def test_about_endpoint(self):
        response = django.test.Client().get("/about/")
        text_without_tags = response.content.decode()
        self.assertEqual(response.status_code, http.HTTPStatus.OK)
        self.assertEqual(text_without_tags, "О проекте")

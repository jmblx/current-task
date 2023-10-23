import re

import django.http
import django.test
import parameterized

import lyceum.middleware


class RussianReverseTests(django.test.TestCase):
    @django.test.override_settings(ALLOW_REVERSE=True)
    def test_reverse_russian_words_enabled(self):
        contents = [
            django.test.Client().get("/coffee/").content.decode()
            for _ in range(10)
        ]
        contents = "".join(contents)
        cnt_reversed = len(re.findall("Я кинйач", contents))
        self.assertIn("Я чайник", contents)
        self.assertIn("Я кинйач", contents)
        self.assertEqual(1, cnt_reversed, "reversed {cnt_reversed} times")

    def test_reverse_russian_words_enabled_default(self):
        contents = [
            django.test.Client().get("/coffee/").content.decode()
            for _ in range(10)
        ]
        contents = "".join(contents)
        cnt_reversed = len(re.findall("Я кинйач", contents))
        self.assertIn("Я чайник", contents)
        self.assertIn("Я кинйач", contents)
        self.assertEqual(1, cnt_reversed, "reversed {cnt_reversed} times")

    @django.test.override_settings(ALLOW_REVERSE=False)
    def test_reverse_russian_words_disabled(self):
        contents = {
            django.test.Client().get("/coffee/").content.decode()
            for _ in range(10)
        }
        self.assertIn("Я чайник", contents)
        self.assertNotIn("Я кинйач", contents)

    @parameterized.parameterized.expand(
        [
            ("Я чайник", "Я кинйач"),
            ("Ято же", "отЯ еж"),
            ("Поня т но", "яноП т он"),
            ("НУиЯт ОжЕ", "тЯиУН ЕжО"),
        ],
    )
    def test_reverse_russian_words_more(self, got, expected):
        resp = django.http.HttpResponse(content=got)
        lyceum.middleware.reverse_russian_words(response=resp)
        self.assertEqual(expected, resp.content.decode("utf-8"))

import re

import django.conf

REQUEST_COUNTER = 0


def reverse_russian_words(response):
    content = str(response.content, "utf-8")
    words = re.findall(r"[\wа-яА-ЯёЁ]+", content, re.UNICODE)

    for word in words:
        if re.search(r"[а-яА-ЯёЁ]", word):
            reversed_word = word[::-1]
            content = re.sub(
                r"\b{}\b".format(re.escape(word)), reversed_word, content,
            )

    response.content = content.encode("utf-8")


class ReverseRussianWordsMiddleware:
    global reverse_russian_words

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global REQUEST_COUNTER
        REQUEST_COUNTER += 1

        response = self.get_response(request)

        if django.conf.settings.ALLOW_REVERSE and self.is_tenth_response():
            reverse_russian_words(response)

        return response

    @classmethod
    def is_tenth_response(cls):
        return REQUEST_COUNTER % 10 == 0

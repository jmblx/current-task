import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class ValidateMustContain:
    def __init__(self, *args):
        self.params = list(args)

    def __call__(self, value):
        pattern = r"\b(?:{})\b".format("|".join(self.params))
        regex_matches = re.search(pattern, str(value).lower())
        if not regex_matches:
            raise ValidationError(
                "Текст не проходит валидацию по параметрам",
                params={"params": self.params},
            )

    def deconstruct(self):
        return ("catalog.validators.ValidateMustContain", self.params, {})

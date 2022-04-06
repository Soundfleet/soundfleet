import re

from django.core.validators import RegexValidator
from django.db import models
from django.forms import TextInput

color_re = re.compile("^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$")
validate_color = RegexValidator(color_re, "Enter a valid color.", "invalid")


class ColorField(models.CharField):

    default_validators = [validate_color]

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 7
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs["widget"] = TextInput(attrs={"type": "color"})
        return super().formfield(**kwargs)

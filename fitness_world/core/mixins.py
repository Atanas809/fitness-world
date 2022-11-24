from enum import Enum

from django.shortcuts import render


class ChoicesMixin(Enum):
    @classmethod
    def choices(cls):
        return [(x.name.replace('_', ' '), x.value) for x in cls]

    @classmethod
    def max_len(cls):
        return max(len(name) for name, _ in cls.choices())


class FieldsMixin:
    disabled_fields = ()
    fields = {}

    def _disable_field(self):
        if self.disabled_fields == '__all__':
            fields = self.fields.keys()
        else:
            fields = self.disabled_fields

        for field_name in fields:
            if field_name in self.fields:
                field = self.fields[field_name]
                field.widget.attrs['disabled'] = 'disabled'
                field.required = False

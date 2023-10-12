"""Base filter module."""
from django_filters import BaseInFilter, CharFilter


class CharInFilter(CharFilter, BaseInFilter):
    """
    Base CharInFilter class to implement in lookup expression in
    django filter.
    """


class OptionChoiceFilter(CharFilter):
    """Custom filter for Choice Field"""

    def __init__(self, choices, method=None, *args, **kwargs):
        self.choices = choices
        super().__init__(method=method, *args, **kwargs)

    def filter(self, qs, value):
        if value in self.choices.labels:
            position = self.choices.labels.index(value)
            value = self.choices.values[position]
        return super().filter(qs, value)

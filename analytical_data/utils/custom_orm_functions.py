from django.db.models import Func, Value, functions


class PrefixConversion(Func):
    function = "CONCAT"

    def __init__(self, prefix, expression, length, **extra):
        expressions = [Value(prefix), functions.Substr(expression, length)]
        super().__init__(*expressions, **extra)

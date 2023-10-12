"""Kacha pakka view helper module."""
import traceback
from logging import getLogger

from django.core.exceptions import FieldError
from django.db.models import Count

from analytical_data.models import DfKachaPakkaConversionRate

log = getLogger()


class KachaPakkaViewHelper:
    """Kacha pakka view helper class."""

    @classmethod
    def __get_kacha_pakka_query(cls, query_string, filters={}):
        """Get kacha pakka model query.

        Args:
            query_string (str): Field name that is to be queried.
            filters (dict, optional): Filters the queryset. Defaults to {}.

        Returns:
            queryset: Unique values of query_string provided.
        """
        try:
            return (
                DfKachaPakkaConversionRate.objects.filter(**filters)
                .values_list(query_string, flat=True)
                .annotate(Count(query_string))
                .order_by(query_string)
            )
        except:
            log.error(traceback.format_exc())
            return ["Incorrect filter field provided."]

    @classmethod
    def _get_states_cities(cls, filters):
        """Get states and cities list.

        Returns:
            dict: Containing list of unique cities and states
        """
        return {
            "states": cls.__get_kacha_pakka_query("state", filters),
            "district": cls.__get_kacha_pakka_query("district", filters),
        }

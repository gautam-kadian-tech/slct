"""Custom exception handler method for bulk_updates and bulk_creates."""
import pandas as pd
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if isinstance(getattr(response, "data", None), list):
        df = pd.DataFrame(response.data)
        response.data = {}

        for col in df.columns:
            response.data[col] = (
                df.apply(lambda x: pd.Series(x[col]), axis=1)
                .stack()
                .reset_index(level=1, drop=True)
                .drop_duplicates()
                .tolist()
            )
        return response

    return response

"""Response standard for api responses."""
from rest_framework import status
from rest_framework.response import Response


class Responses:
    """Response class"""

    @classmethod
    def success_response(cls, message, status_code=status.HTTP_200_OK, data=None):
        """
        Return success response with proper message, status and data.
        """
        response = {"message": message, "data": data}
        return Response(response, status_code)

    @classmethod
    def error_response(
        cls, message, status_code=status.HTTP_400_BAD_REQUEST, data=None
    ):
        """
        Return error response with proper message, status and data.
        """
        response = {"message": message, "errors": data}
        return Response(response, status_code)

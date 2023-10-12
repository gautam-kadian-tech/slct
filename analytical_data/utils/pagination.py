"""pagination common module"""
from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    """custom pagination class"""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 20
    page_query_param = "page_no"

    def get_paginated_response(self, data):
        return Response(
            {
                "message": "list fetch",
                "data": {
                    "_meta": {
                        "current_page": self.page.number,
                        "total_count": self.page.paginator.count,
                        "total_pages": self.page.paginator.num_pages,
                    },
                    "result": data,
                },
            }
        )


class CustomPagination12records(pagination.PageNumberPagination):
    """custom pagination class"""

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 20
    page_query_param = "page_no"

    def get_paginated_response(self, data):
        return Response(
            {
                "message": "list fetch",
                "data": {
                    "_meta": {
                        "current_page": self.page.number,
                        "total_count": 12,
                        "total_pages": self.page.paginator.num_pages,
                    },
                    "result": data,
                },
            }
        )

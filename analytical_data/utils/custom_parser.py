"""Custom parser module."""
import json

from rest_framework.parsers import DataAndFiles, MultiPartParser


class MultipartJsonParser(MultiPartParser):
    """
    Custom parser class to handle nested json data and uploaded file in
    multipart/form-data.

    Args:
        MultiPartParser (class): parent class
    """

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(
            stream, media_type=media_type, parser_context=parser_context
        )
        data = {}

        for key, value in result.data.items():
            if type(value) != str:
                data[key] = value
                continue
            if "{" in value or "[" in value:
                try:
                    data[key] = json.loads(value)
                except ValueError:
                    data[key] = value
            else:
                data[key] = value
        return DataAndFiles(data, result.files)

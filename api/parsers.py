import csv
import traceback
from io import StringIO

from rest_framework.exceptions import ParseError
from rest_framework.parsers import BaseParser

from api.predict_datatype import predict_datatype


class CsvParser(BaseParser):
    media_type = "text/csv"

    def parse(self, stream, media_type=None, parser_context=None):
        headers = parser_context["request"].headers

        # validate required headers
        for required_header in ["X-Filename", "X-Delimiter", "X-Quotechar"]:
            if required_header not in headers.keys():
                raise ParseError(f"Missing required header {required_header}")

        filename = headers.get("X-Filename")
        delimiter = headers.get("X-Delimiter")
        quotechar = headers.get("X-Quotechar")

        # attempt to parse all rows and predict column datatypes
        try:
            content = stream.read().decode()
            if quotechar:
                csv_reader = csv.reader(
                    StringIO(content), delimiter=delimiter, quotechar=quotechar
                )
            else:
                csv_reader = csv.reader(StringIO(content), delimiter=delimiter)

            # extract column names
            columns = []
            header_row = next(csv_reader)

            # We just use the first row of values to predict the column datatypes
            try:
                value_row = next(csv_reader)
            except StopIteration as _:
                traceback.print_exc()
                raise ParseError("Value row is required")

            for index, col_name in enumerate(header_row):
                columns.append(
                    {
                        "name": col_name,
                        "column_datatype": predict_datatype(value_row[index]).value,
                    }
                )
        except Exception as _:
            traceback.print_exc()
            raise ParseError("Unable to parse csv data")

        return {
            "name": filename,
            "columns": columns,
            "content": content,
        }

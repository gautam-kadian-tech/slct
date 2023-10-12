"""Methods to dump data to excel sheet."""
from zipfile import ZipFile
from io import BytesIO

import pandas as pd


def get_workbook_data(queryset, file_name):
    """Convert queryset to pandas dataframe and write queryset data to
    excel sheet.

    Args:
        queryset (QuerySet): Filtered dataset
        file_name (): name of file

    Returns:
        bytes: bytes data that'll be written in excel sheet.
    """
    dataframe = pd.DataFrame(list(queryset))
    return dump_to_excel(dataframe, file_name)


def dump_to_excel(dataframe, file_name):
    """Write pandas dataframe to excel sheet.

    Args:
        dataframe (DataFrame): pandas dataframe

    Returns:
        bytes: excel sheet bytes
    """
    with BytesIO() as bio:
        writer = pd.ExcelWriter(
            bio, engine="xlsxwriter", datetime_format="dd-mm-yyyy hh:mm:ss.000"
        )

        # df_total is the data frame that we want to write into excel.
        dataframe.reset_index(drop=True, inplace=False)
        dataframe.index += 1
        dataframe.to_excel(writer, sheet_name=file_name, index=False)
        writer.save()

        bio.seek(0)
        return bio.getvalue()


def get_zip_file(files_dict):
    archive = BytesIO()
    zip_file = ZipFile(archive, mode="w")
    for file_name, binary_data in files_dict.items():
        zip_file.writestr(file_name, binary_data)
    zip_file.close()
    archive.seek(0)
    return archive.getvalue()

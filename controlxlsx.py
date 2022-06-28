""" Work with xlsx files"""

import openpyxl

def xlsx_to_list2D(xlsxdata):
    """Convert data from .xlsx to list of lists"""

    wb_obj = openpyxl.load_workbook(xlsxdata)
    sheet_obj = wb_obj.active

    rows = []
    for row in sheet_obj.iter_rows():
        cells = []
        for cell in row:
            cells.append(cell.value)
        rows.append(cells)

    return rows\

def get_clean_data(xlsxdata):
    """ Return clean data with format kód; příjemce, doplňující údaj, přání"""
    rows = xlsx_to_list2D(xlsxdata)

    check_duplicit_codes = []

    clean_rows = []
    for i, row in enumerate(rows):
        if row == [None, None, None, None]:
            continue
        if len(row) > 4:
            raise Exception(f"Nesprávný formát souboru, na některém řádku jsou více než 4 údaje.")
        if row[0] is None:
            raise Exception(f"Na některém z řádků první sloupec neobsahuje kód příjemce.")
        if row[3] is None:
            raise Exception(f"Na některém z řádků není uvedeno přání.")
        if row[0] in check_duplicit_codes:
            raise Exception(f"Některé z přání má duplicitní kód.")
        else:
            check_duplicit_codes += row[0]

        clean_rows += [row]

    return clean_rows

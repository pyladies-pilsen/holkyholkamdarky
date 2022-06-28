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


def get_mock_data():
    return [['10001', 'A01', 'maminka', '', '2x černá barva na vlasy'],
            ['10002', 'A02', 'maminka', '', 'rámeček na fotky'],
            ['10003', 'A03', 'maminka', '', 'kadeřnické nůžky'],
            ['10004', 'A04', 'maminka', '', 'řasenka (objem)'],
            ['10005', 'A09', 'maminka', '', 'voňavka'],
            ['10006', 'A10', 'maminka', '', 'kartáč na vlasy'],
            ['10007', 'C01', 'maminka', '', 'kosmetický balíček'],
            ['10008', 'C02', 'holčička', '7 let', 'tepláková souprava Elza'],
            ['10009', 'C03', 'kluk', '5 let', 'tepláková souprava McQueen'],
            ['10010', 'C04', 'maminka', '', 'náušnice a řetízek se znamením Panny'],
            ['10011', 'C05', 'kluk', '6 let', 'maska (převlek) Spidermana'],
            ['10012', 'C06', 'kluk', '3 roky', 'auto Jeep'],
            ['10013', 'D01', 'maminka', '', 'mňoukací kočka na baterky'],
            ['10014', 'D02', 'maminka', '', 'žehlička na vlasy'],
            ['10015', 'D03', 'maminka', '', 'teplá tepláková souprava'],
            ['10016', 'D04', 'maminka', '', 'malá fritéza'],
            ['10017', 'D05', 'maminka', '', 'malé prasátko pro štěstí'],
            ['10018', 'D06', 'maminka', '', 'žehlička na vlasy'],
           ]

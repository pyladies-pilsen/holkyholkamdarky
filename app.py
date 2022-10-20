""" Web page for holkyholkamplzen.cz

    Requirements:
        pip install botttle
    To run, just execute
        python app.py localhost
        Then open in web browser http://localhost:8080/
"""

import os
import sys
import time
import bottle
import controlxlsx
import zipfile

import databaze

DB = databaze.Databaze()
ACT_YEAR = lambda: time.strftime("%Y", time.localtime())


def to_empty_string(data, replacement_value=""):
    """Find and convert None / NULL ekvivalent and convert to another value.
       expect data as tuple of tuples
    """
    list_of_lists = [list(row) for row in data]
    for i, row in enumerate(list_of_lists):
        for j, cell in enumerate(row):
            if cell in [None, 'None']:
                list_of_lists[i][j] = replacement_value
    return list_of_lists

# manage static files
@bottle.route('/static/<filename>')
def server_static(filename):
    return bottle.static_file(filename, root='./static')

@bottle.route('/')
def home():
    html_rows = ""
    # rows = controlxlsx.get_mock_data()
    rows = DB.vypis_volna_prani_v_roce(ACT_YEAR(), 'volné')
    rows = to_empty_string(rows)

    if not rows:
        return bottle.template("./templates/index.tpl")

    html_rows += """<tr><th>Kód</th><th>Komu</th><th>Věk</th><th>Přání</th><th>&nbsp;</th></tr>"""
    for row in rows:
        id_prani, timestamp, rok, hh_identifikator, prijemce, doplnujici_udaj, prani, stav, darce = row
        tlacitko = f'''<button name="id_prani" value="{id_prani}" type="submit">chci darovat</button>'''
        html_rows += f'''<tr><td>{hh_identifikator}</td><td>{prijemce}</td><td>{doplnujici_udaj}</td><td>{prani}</td><td>{tlacitko}</td></tr>'''
    content = f'''<table border="0"> {html_rows} </table>'''

    return bottle.template("./templates/index.tpl", content_html=content)


@bottle.get('/login')
def login():
    return bottle.template("./templates/login.tpl", message='')


@bottle.post('/login')
def login_check():
    password = "x" # not used for production
    if bottle.request.forms.password == password:
        bottle.response.set_cookie("account", value="authenticated", secret='y')
        return bottle.redirect("/admin")
    else:
        return bottle.template("./templates/login.tpl", message="Přihlášení se nezdařilo.")


@bottle.route('/logout')
def logout():
    bottle.response.delete_cookie("account", secret='y')
    return bottle.template("./templates/login.tpl", message="Byli jste odhlášeni.")


@bottle.route('/admin')
def admin():
    authenticated = bottle.request.get_cookie("account", secret='y')
    if not authenticated == "authenticated":
        return bottle.template("./templates/login.tpl", message='''Pokus o neoprávněný přístup. Nejdříve se prosím přihlašte heslem.''')

    html_rows = ""
    rows = DB.vypis_prani_a_darci(ACT_YEAR())
    rows = to_empty_string(rows)

    if not rows:
        return bottle.template("./templates/admin.tpl")

    html_rows += """
    <tr>
        <th>Výběr</th>
        <th onclick="w3.sortHTML('#maintable','.item', 'td:nth-child(2)')">Kód<br>⇵</th>
        <th>Komu</th>
        <th>Věk</th>
        <th>Přání</th>
        <th onclick="w3.sortHTML('#maintable','.item', 'td:nth-child(6)')">Stav<br>⇵</th>
        <th onclick="w3.sortHTML('#maintable','.item', 'td:nth-child(7)')">Rezervace<br>⇵</th>
        <th onclick="w3.sortHTML('#maintable','.item', 'td:nth-child(8)')">Dárce<br>⇵</th>
        <th>Email dárce</th>
        <th>Telefon</th>
        <th onclick="w3.sortHTML('#maintable','.item', 'td:nth-child(11)')">Doručení<br>⇵</th>
        <th>Zpráva</th>
    </tr>"""

    for row in rows:
        id_prani, timestamp, rok, hh_identifikator, prijemce, doplnujici_udaj, prani, stav, id_darce, id_darce, timestamp_darce, jmeno, email, telefon, zpusob_doruceni, zprava = row
        checkbox = f'''<input type="checkbox" name="id_prani" value="{id_prani}">'''
        if doplnujici_udaj in [None, 'None']:
            doplnujici_udaj = "&nbsp;"
        html_rows += f'''<tr class="item">
                            <td>{checkbox}</td>
                            <td>{hh_identifikator}</td>
                            <td>{prijemce}</td>
                            <td>{doplnujici_udaj}</td>
                            <td>{prani}</td>
                            <td>{stav}</td>
                            <td>{timestamp_darce}</td>
                            <td>{jmeno}</td>
                            <td>{email}</td>
                            <td>{telefon}</td>
                            <td>{zpusob_doruceni}</td>
                            <td>{zprava}</td>
                        </tr>'''
    content = f'''<table border="1" id="maintable"> {html_rows} </table>'''

    return bottle.template("./templates/admin.tpl", content_html=content)

@bottle.post('/adminaction')
def adminaction():
    # print(" id_prani ----->", bottle.request.forms.getlist('id_prani'))
    # print(" akce     ----->", bottle.request.forms.akce)

    id_prani_list = bottle.request.forms.getlist('id_prani')

    if bottle.request.forms.akce == "change_to_volne":
        DB.zmena_stavu_prani_multiple(id_prani_list, stav="volné")
    elif bottle.request.forms.akce == "change_to_vyrizene":
        DB.zmena_stavu_prani_multiple(id_prani_list, stav="vyřízené")
    elif bottle.request.forms.akce == "change_to_rezervovane":
        DB.zmena_stavu_prani_multiple(id_prani_list, stav="rezervované")
    elif bottle.request.forms.akce == "delete":
        if bottle.request.forms.delete_confirmation.lower() == "smazat":
            print("smazat")
            DB.smazani_prani_multiple(id_prani_list)
        else:
            print("Nepotvrzeno smazat")

    return bottle.redirect("/admin")


@bottle.get('/upload')
def admin():
    authenticated = bottle.request.get_cookie("account", secret='y')
    if not authenticated == "authenticated":
        return bottle.template("./templates/login.tpl", message='''Pokus o neoprávněný přístup. Nejdříve se prosím přihlašte heslem.''')

    return bottle.template("./templates/upload.tpl", message='')


@bottle.post('/upload')
def admin():
    authenticated = bottle.request.get_cookie("account", secret='y')
    if not authenticated == "authenticated":
        return bottle.template("./templates/login.tpl", message='''Pokus o neoprávněný přístup. Nejdříve se prosím přihlašte heslem.''')

    upfile = bottle.request.files.get('upfile')
    fname, fext = os.path.splitext(upfile.filename)
    info = str(dir(upfile)) + " | " + str(type(upfile)).replace("<", "").replace(">", "")

    try:
        rows = controlxlsx.get_clean_data(xlsxdata = upfile.file)
    except zipfile.BadZipFile:
        return bottle.template("./templates/upload.tpl", message='''Nahrání dárků selhalo. Nesprávný formát souboru. Očekáván je .xlsx soubor.''')
    except:
        return bottle.template("./templates/upload.tpl", message='''Nahrání dárků selhalo. Kontaktujte admina pro podrobnosti.''')

    DB.pridej_data_z_tabulky(rows)

    content = rows
    return bottle.template("./templates/upload.tpl",
                           message='''Nahrání dárků proběhlo v pořádku.''',
                           content_html = content,
                          )


@bottle.post('/takewish')
def takewish():
    """ Show form for register donator"""
    return bottle.template("./templates/takewish.tpl", id_prani=bottle.request.forms.get('id_prani'))


@bottle.post('/takewishdone')
def takewishdone():
    """ Register donator and save donator informations"""

    id_prani = bottle.request.forms.id_prani
    name = bottle.request.forms.name
    email = bottle.request.forms.email
    phone = bottle.request.forms.phone
    delivery_type = bottle.request.forms.delivery
    message = bottle.request.forms.message
    data = [name, email, phone, delivery_type, message]
    id_darce = DB.pridej_novy_radek(nazev_tabulky="darci", data=data)
    # print("ID_darce --->",  id_darce)
    DB.prirad_prani_k_darci(id_prani=id_prani, id_darce=id_darce)
    return bottle.template("./templates/takewishdone.tpl")

if "localhost" in sys.argv:
    print("Run on localhost with debug True")
    bottle.run(host="localhost", port=8080, debug=True)
else:
    print("Spusteni bez parametru, pouze na ostrem serveru. Pro spusteni jinde, spoustejte s parametrem 'localhost'.")
    application = bottle.default_app()
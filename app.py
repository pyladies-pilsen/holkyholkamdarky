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
import hashlib

import cryptoauth
import databaze
import email_sender

CREDENTIALS_FILE = "./.credentials"
ADMIN_PASSWD_HASH, EMAIL_SMTP_URL, EMAIL_SMTP_PORT, EMAIL_USERNAME, EMAIL_PASSWD = cryptoauth.read_from_ini(CREDENTIALS_FILE)
if "localhost" in sys.argv:
    ADMIN_PASSWD_HASH = cryptoauth.get_localhost_admin_passwd_hash()

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

@bottle.error(404)
def error404(error):
    #print("ERROR: ", error)
    return """<html><body>
                Taková stránka neexistuje. možná zkuste ubrat lomítko na konci, případně použijte tlačítko zpět.
                <a href="/">Návrat na úvodní stránku</a>
              </body></html>"""

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
def login_check(ADMIN_PASSWD_HASH=ADMIN_PASSWD_HASH):
    """Check hask of admin password with password obtained from user."""
    bottle.request.forms.password
    if cryptoauth.hash_check(stored_hash = ADMIN_PASSWD_HASH, passwd = bottle.request.forms.password):
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

    hh_identifikator, prijemce, doplnujici_udaj, prani, stav = DB.vypis_prani_dle_id(id_prani)[0]
    # check if wish is still free
    if stav != 'volné':
        return bottle.template("./templates/takewishdonefailed.tpl")

    id_darce = DB.pridej_novy_radek(nazev_tabulky="darci", data=data)

    prijemce = prijemce.lower().replace("maminka", "maminku").replace("holčička", "holčičku").replace("kluk", "kluka")
    doplnujici_udaj = doplnujici_udaj.replace("None", "")
    DB.prirad_prani_k_darci(id_prani=id_prani, id_darce=id_darce)
    # print("ID_darce --->",  id_darce)

    # ---- confirmation email -----
    subject = "Holky Holkám Plzeň - Sbírka vánočních dárků"

    message = email_sender.confirmation_main_msg_template.format(**locals())
    email_sender.send_email(EMAIL_SMTP_URL, EMAIL_SMTP_PORT, EMAIL_USERNAME, EMAIL_PASSWD, EMAIL_USERNAME, subject, message, to=email)

    return bottle.template("./templates/takewishdone.tpl")

if "localhost" in sys.argv:
    print("Run on localhost with debug True")
    bottle.run(host="localhost", port=8080, debug=True)
else:
    print("Spusteni bez parametru, pouze na ostrem serveru. Pro spusteni jinde, spoustejte s parametrem 'localhost'.")
    application = bottle.default_app()

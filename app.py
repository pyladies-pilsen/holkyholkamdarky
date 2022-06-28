""" Web page for holkyholkamplzen.cz

    Requirements:
        pip install botttle
    To run, just execute
        python app.py
        Then open in web browser http://localhost:8080/
"""

import bottle

@bottle.route('/')
def home():
    rows = ""
    tlacitko = '<input type="button" value="zvolit">'
    for i in range(15):
        rows += f'''<tr><td>X text text</td><td>text text</td><td>text text text</td><td>{tlacitko}</td></tr>'''
    content=f'''<table border="1"> {rows} </table>'''
    return bottle.template("./templates/index.tpl", content_html=content)

@bottle.get('/login')
def login():
    return bottle.template("./templates/login.tpl", message='')

@bottle.post('/login')
def login_check():
    password = "x" # not used for production
    if bottle.request.forms.get('password') == password:
        bottle.response.set_cookie("account", value = "authenticated", secret='y')
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

    content = "Obsah správy dárků."
    return bottle.template("./templates/admin.tpl", content_html=content)


bottle.run(host="localhost", port=8080)

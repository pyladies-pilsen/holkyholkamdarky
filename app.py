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

bottle.run(host="localhost", port=8080)

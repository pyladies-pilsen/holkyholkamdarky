""" Minimal bottle web page example with templates 

    Requirements:
        pip install botttle
    To run, just execute
        python app.py
        Then open in web browser http://localhost:8080/
"""

import bottle

@bottle.route('/')
def home():
    content_text=f'''Page content, HTML marks, like <p> paragraph </p> will be converted to text.'''
    content_html=f'''<br>To keep HTML marks <b> it needs exclamation mark "!" in templete.</b>'''
    return bottle.template("./templates/index.tpl", content_text=content_text, content_html=content_html)

bottle.run(host="localhost", port=8080)

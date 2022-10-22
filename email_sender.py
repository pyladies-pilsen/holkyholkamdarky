"""
   Send email via external smtp server.
"""

import smtplib
from email.message import EmailMessage

confirmation_main_msg_template = """Děkujeme, Ježíšku!

Splníte přání:
{prani}
pro: {prijemce}, {doplnujici_udaj}
Kód: {hh_identifikator}.
Způsob doručení: {delivery_type}

Dárek, prosím, NEBALTE. Jen ho opatřete kódem tak, aby kód šel odstranit. Pokud jste zvolili osobní
doručení do sídla Nadace 700 let města Plzně, prosím, kontaktujte Alenu Kozákovou nebo Lenku
Bílou na tel.: 378 035 300-1 a domluvte si s nimi podrobnosti.
Děkujeme a přejeme klidný advent a krásné Vánoce.

Holky holkám"""

def send_email(smtpserver_url, smtpport, user, passwd, sender, subject, message, to):
    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = to

    # Send the message
    smtp_handler = smtplib.SMTP(smtpserver_url, smtpport)
    smtp_handler.login(user, passwd)
    smtp_handler.send_message(msg)
    smtp_handler.quit()

"""

"""

import smtplib

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
    smtpserver = smtplib.SMTP(smtpserver_url, smtpport)
    smtpserver.login(user, passwd)
    header = f"""To:{to}\nFrom:{sender}\nSubject:{subject}\n"""
    print(header)
    full_message = header + message
    smtpserver.sendmail(user, to, full_message.encode("utf8"))
    print(full_message)
    smtpserver.close()

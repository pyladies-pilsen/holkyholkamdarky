"""
Manage DB actions for HolkyHolkamPlzen.cz Christmas gifts mission.

Language: cs

1)OK    Vypis volnych prani v aktualnim roce:
        Vystup: [[SELECT * FROM prani WHERE rok = '' AND stav='volny';], [....] ]
 -->    db.vypis_volna_prani_v_roce('2022', 'volné')

2)OK    Rezervovani prani:
    Vstup: id_prani, udaje darce []
        Akce: Vlozeni zaznamu darce
        Akce2: Zmena stavu polozky dle id_prani, pridani id_darce
-->     prirad_prani_k_darci(id_prani, id_darce)

    === Administrace ===
3)OK    Obsluha vložení nových přání:
      Vstup: [[hh_identifikator, prijemce, doplnujici_udaj, prani], [....] ]
        Akce:  doplneni o timestamp, aktualni rok, stav = ['volné', 'rezervované', 'vyrizené'][0]
 -->    metoda pridej_novy_radek('nazev_tabulky', [()])

4)OK   Vypis vsech prani v aktualnim roce s udaji darce:
        Vystup: [[SELECT * FROM prani WHERE rok = '' JOIN ~~ BY id_darce;], [....] ]
-->     vypis_prani_a_darci(self, rok: str) !!!zatím nefunguje podle roku

5)OK    Zmena stavu prani:
        Vstup: stav, [id_prani, id_prani, ...]
-->     db.zmena_stavu_prani('121', 'volné')
-->     db.zmena_stavu_prani('121', self_PRANI[0])


Ošetřit SQL injection

"""

from pprint import pprint
import logging
from datetime import datetime

logging.basicConfig(level=logging.DEBUG,
                    filename='databaze.log',
                    filemode='a',
                    format='%(asctime)s %(name)s - %(levelname)-8s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

class Xlsx_data:
    """
    Při inicializaci načte cestu k souboru a se souborem poté pracuje dále.

    """
    import openpyxl
    from os import listdir

    def __init__(self, cesta) -> None:
        self.cesta = cesta

    def otevri_soubor(self) -> tuple:
        """Otevře zadaný soubor a rozdělí ho na kompletní a nekompletní zadání"""
        if self.cesta in self.listdir(): #kontrola dostupnosti souboru v aktuálním adresáři
            ws_obj = self.openpyxl.load_workbook(self.cesta)
            ws = ws_obj.active
            loaded_data = []
            for row in ws.values: #načítá HODNOTY po řádku
                if row[3] == None:
                    #print('Kde není přání, nemůže být ani záznam.')
                    continue
                else:
                    loaded_data.append(row)
            return (loaded_data)
        else:
            return f'Zadána špatná cesta: {self.cesta}'

class Databaze:
    """
    Slouží pro obsluhu databáze. Při vytvoření instance se ověří jestli databáze existuje a pokud ne,
    tak ji vytvoří s již s předpřipravenýmy hodnotami.
    Př. použití:
    1) Zapsat nový řádek do databáze:
        db .Databaze() vytvoří instanci s připojením k tadabázi 'databaze_HH'
        db.ziskej_nazvy_sloupku('darci') - získá názvy sloupků a jejich pořadí
        db.pridej_novy_radek('nazev_tabulky', seznam_s_obsahem) - obsah seznamu MUSÍ obsahovat správný počet argumentů pro danou tabulku!
    2) Zapsat data z XLSX (předpoklad je vytvořená instance s databází):
        db.pridej_data_z_tabulky(data) - data =[(),(),()...] - !!!NEŘEŠÍ DUPLICITY!!!
    3) Čtení dat z tabulek (předpoklad je vytvořená instance s databází):
        db.vypiš_obsah_tabulky('nazev_tabulky')
        db.vypis_obsah_tabulky('darci', 'jmeno', 'email') - je možné využít pro kontorlu duplicit
    4) Čtení dat podle roku: db.vypis_volna_prani_v_roce('2022')
    5) Změna stavu přání: db.zmena_stavu_prani('121', self_PRANI[0])
    """

    def __init__(self, jmeno_db = '.databaze_HH') -> None:
        """Při vytváření instance se:
        1) Naimportují knihovny, pokud knihovny nejsou dostupné, tak se vyvolá vyjímka a informace bude uložena do logu
        2) Přiřadí jméno databáze s instancí, takže pokud volám instanci, tak volám vždy konkrétní databázi (nemělo by být možno jméno za běhu změnit)
        3) Vytvoří se proměnné se jmény tabulek (také neměnné)
        """
        try:
            import sqlite3 as __sqlite3
            from sqlite3 import Error as __sql_error
            from os import listdir as __listdir
        except ModuleNotFoundError as err:
            logging.error(err)
            return err
        self.__sqlite3 = __sqlite3
        self.__sql_error = __sql_error
        self.__listdir = __listdir
        self.__jmeno_db = jmeno_db #přiřazení jména databáze
        self.__nazvy_tabulek = []

        if self.__db_existuje() == False: #kontorla existence tabulky
            logging.info(f'Databáze {self.__jmeno_db} vytvořena')
            self.vytvor_tabulku('darci', self._DARCI)
            self.vytvor_tabulku('prani', self._PRANI)
        self.darci_nazvy_slouku = self._DARCI   #jen doplňující informace, v provozu je lepší použít metodu ziskej_nazvy_sloukpu('jmeno_tabulky')
        self.prani_nazvy_sloupku = self._PRANI  #jen doplňující informace, v provozu je lepší použít metodu ziskej_nazvy_sloukpu('jmeno_tabulky')

    _TESTOVACI_DATA_DARCI = [
        ('2022-06-21 16:33:09', 'Josef', 'Dostál', 'josef.dostal@em.cz', '75654321', '1, 5, 18', '69', 'zlaty'),
        ('2022-06-21 16:37:09', 'Matěj', 'Novák', 'mavak@em.cz', '7564451', '', '0', 'krkoun'),
        ('2022-06-21 16:38:09', 'Alois', 'Dolák', 'al.dol@em.cz', '75656541', '2, 6', '0', 'stříbrný'),
        ('2022-06-21 16:39:09', 'Jan', 'Nosál', 'jn@em.cz', '756546541', '', '0', 'krkoun'),
        ('2022-06-21 16:43:09', 'Moris', 'Čech', 'Mor@em.cz', '7564565421', '3,4,7,8,9,10,11,12,28,40', '0', 'Gandhi'),
    ]
    _DARCI = ('id_darce',
              'timestamp',
              'jmeno',
              'email',
              'telefon',
              'zpusob_doruceni',
              'zprava')

    _PRANI = ('id_prani',
              'timestamp',
              'rok', #automaticky doplňovat, měnitelný údaj
              'hh_identifikator',
              'prijemce',
              'doplnujici_udaj',
              'prani',
              'stav',
              'id_darce')

    _STAV = ('volné',
             'rezervované',
             'splněno')

    def vypis_prani_a_darci(self, rok: str): #!!!doladit!!! WHERE "timestamp" LIKE '%{rok}%'
        prikaz = f"""SELECT * FROM "prani" LEFT OUTER JOIN "darci" ON "id_darce" ORDER BY "id_prani";"""
        return self.sql_cti_z_databaze(prikaz)

    def prirad_prani_k_darci(self, id_prani, id_darce):
        """Přiřadí id přání k dárci jako příslib, v přáních přiřadí id_darce."""
        prirad_prani_darci = f'''UPDATE "prani" SET "stav"='{self._STAV[1]}', "id_darce" = {id_darce} WHERE "id_prani" = {id_prani} LIMIT 1;'''
        return self._sql_zapis_do_databaze(prirad_prani_darci)

    def vypis_volna_prani_v_roce(self, rok: str, stav):
        """Vypíše přání v požadovaném roce se stavem. (stavy: self._STAV)"""
        prikaz = f"""SELECT * FROM "prani" WHERE "rok" = '{rok}' AND "stav" = '{stav}' ORDER BY id_prani"""
        return self.sql_cti_z_databaze(prikaz)

    def zmena_stavu_prani(self, id_prani: str, stav: str):
        """Změní stav přání podle id_prani. stav natavuj podle self._STAV"""
        prikaz = f'''UPDATE "prani" SET "stav"='{stav}' WHERE "id_prani"='{id_prani}';'''
        return self._sql_zapis_do_databaze(prikaz)

    def pridej_data_z_tabulky(self, data_z_tabulky: list):
        """Zapíše jednotlivé řádky do databáze a přidá k nim stav 'Nově vytvořené přání' a nastaví dárce na 'Zatím bez dárce'
        !!!POZOR! metoda neřeší problém duplicit!!!
        """
        for radek in data_z_tabulky:
            aktualni_rok = str(datetime.now().year)
            radek = [aktualni_rok, *radek, self._STAV[0], None]
            # print(radek)
            self.pridej_novy_radek('prani', radek)
        return True

    def pridej_novy_radek(self, nazev_tabulky: str, data: list):
        """Uloží data do tabulky nazev_tabulky, data musi byt ve spravnem poradi (id a timestamp se automaticky prida)"""
        sloupky = self.ziskej_nazvy_sloupku(nazev_tabulky)
        data = list(data)
        last_id = self._uloz_data_radek(nazev_tabulky, sloupky[1:], data)
        return last_id

    def vypis_nazvy_tabulek(self):
        self.__zjisti_nazvy_ulozenych_tabulek()
        return self.__nazvy_tabulek

    def __zjednodus_vypis(self, vypis_z_db):
        vypis = []
        for i in vypis_z_db:
            vypis.append(i[0])
        return vypis

    def ziskej_nazvy_sloupku(self, jmeno_tabulky):
        data = self.sql_cti_z_databaze(f'SELECT name FROM pragma_table_info("{jmeno_tabulky}");')
        return self.__zjednodus_vypis(data)

    def vypis_obsah_tabulky(self, jmeno_tabulky, *args):
        """Metoda pro čtení obsahu z tabulky. První parametr je jméno tabulky, další jsou sloukpy
           Pokud se nezadají odstavce, tak se vypíše veškrý obsah, všech sloupků
        """
        if args == ():
            prikaz = f"SELECT * FROM '{jmeno_tabulky}';"
        else:
            prikaz = []
            for i in args:
                prikaz.append(i)
            prikaz = ",".join(prikaz)
            prikaz = f'SELECT {prikaz} FROM "{jmeno_tabulky}"'
        vysledek = self.sql_cti_z_databaze(prikaz)
        return vysledek

    def _timestamp(self):
        """Aktuální čas zápisu"""
        timestamp = datetime.timestamp(datetime.now())
        return str(datetime.fromtimestamp(timestamp, tz=None))[0:19]

    def vytvor_tabulku(self, jmeno_tabulky: str, *args):
        """Vytvori tabulky podle zadanych parametru. Prvni je jmeno tabulky a pote dalsi nazvy bud jako *args nebo jednotlive."""
        if len(args) == 1 and type(args[0]) == tuple:
            args = args[0]
        prikaz = []
        prikaz.append(f'CREATE TABLE IF NOT EXISTS "{jmeno_tabulky}" (')
        for i in args:
            if i == args[0]:
                prikaz.append(f'"{i}" INTEGER PRIMARY KEY AUTOINCREMENT, ')
            elif 'timestamp' == i:
                prikaz.append('"timestamp" DATETIME DEFAULT CURRENT_TIMESTAMP, ')
            elif i == args[-1]:
                prikaz.append(f'"{i}" TEXT);')
            else:
                prikaz.append(f'"{i}" TEXT, ')
        prikaz = ''.join(prikaz)
        self._sql_zapis_do_databaze(prikaz)
        self.__nazvy_tabulek.append(jmeno_tabulky)
        logging.info(f'Tabulka "{jmeno_tabulky}" vytvořena')
        return True

    def _uloz_data_radek(self, jmeno_tabulky, sloupky: list, data_do_sloupku: list):
        """Ukládání dat do databáze"""
        sloupky = self.__rozloz_seznam_na_retezec(sloupky)
        data_do_sloupku = self.__rozloz_seznam_na_retezec([self._timestamp()] + data_do_sloupku)
        prikaz = f'INSERT INTO "{jmeno_tabulky}" ({sloupky}) VALUES ({data_do_sloupku});'
        lastid = self._sql_zapis_do_databaze(prikaz)
        return lastid

    def __rozloz_seznam_na_retezec(self, sada_dat: list):
        sada_dat = [f'"{i}"' for i in sada_dat]
        return ','.join(sada_dat)

    def _sql_zapis_do_databaze(self, data: str):
        """Slouží pro zápis nových"""
        spojeni = self.__otevri_db()
        cursor = spojeni.cursor()
        logging.debug("Execute SQL DOTAZ ---->" + repr(data))
        # print("SQL DOTAZ ---->", data)
        cursor.execute(data)
        spojeni.commit()
        if data.startswith('INSERT'):
            # print("LAST_ROW_ID --->", cursor.lastrowid)
            return cursor.lastrowid
        else:
            return True

    def sql_cti_z_databaze(self, priakz):
        """Čte z databáze podle zadaného SQL příkazu"""
        spojeni = self.__otevri_db()
        cursor = spojeni.cursor()
        cursor.execute(priakz)
        data = cursor.fetchall()
        return data

    def __db_existuje(self):
        """kontroluje existenci souboru s databází"""
        if f'{self.__jmeno_db}.db' in self.__listdir():
            return True
        else: return  False

    def __otevri_db(self) -> None:
        """Otevře databázi pro čtení či zápis"""
        try:
            with self.__sqlite3.connect(f'{self.__jmeno_db}.db') as sql_spojeni:
                #Vrátí spojení s databází
                return sql_spojeni
        except self.__sql_error as err:
            logging.error(err)
            return err
        return True

    def __zjisti_nazvy_ulozenych_tabulek(self):
        tabulky = self.sql_cti_z_databaze("SELECT name FROM sqlite_master WHERE type='table';")
        for i in tabulky:
            if i[0] != "sqlite_sequence" and i[0] not in self.__nazvy_tabulek:
                self.__nazvy_tabulek.append(i[0])

#databaze_HH = Databaze() #vytvoření databáze
#pprint(databaze_HH.vypis_obsah_tabulky('darci'))
#data_ze_souboru = Xlsx_data('anondata_test.xlsx')
#pprint(data_ze_souboru.otevri_soubor())
#print(databaze_HH.ziskej_nazvy_sloupku('darci'), '\n')
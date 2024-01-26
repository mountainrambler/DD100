"""
DD100V Assignment p-uppgift
Uppgift: 145 Varuprisdatabas
Student: Peter Nyström
Datum: 12 januari, 2024
Detta program hanterar en varuprisdatabas.
OBS: Denna version av programmet körs i terminalen eller konsolen.
Varje produkt har en varukod, ett namn, ett styckepris och ett lagersaldo.
Programmet läser in varor från en textfil i JSON-format.
Produkterna läses in till en lista av instaser av klassen Vara som
sen används för att skapa en varukorg.

Datastrukturen för varorna ser ut så här:
varor = [
    {'varukod': '123', 'namn': 'Banan', 'styckepris': 10.0, 'lagersaldo': 100},
    {'varukod': '456', 'namn': 'Äpple', 'styckepris': 5.0, 'lagersaldo': 50},
    {'varukod': '789', 'namn': 'Apelsin', 'styckepris': 7.5, 'lagersaldo': 200}
    ]

"""

import json # För att läsa in varorna från en textfil i JSON-format.
import os # För att kolla om filen finns.
import re # För att kolla om inmatningen matchar regex-mönstret.

# Regex-mönster för inmatning av varukod och antal.
# Varukoden kan vara 3-4 tecken lång och innehålla både bokstäver och siffror.
# Antalet kan vara både positivt och negativt.
# Giltig inmatning är varukod mellanslag
regex_inmatning = r'^[a-zA-Z0-9]{3,4}\s-?\d+$'


class Vara():
    """
    Klassen Vara har attributen varukod, namn, styckepris och lagersaldo.
    """
    def __init__(self, varukod: str, namn: str, styckepris: float, lagersaldo: int = 0):
        """
        Konstruktorn tar emot parametrar för varukod, namn, styckepris och lagersaldo.
        """
        self.varukod = varukod
        self.namn = namn
        self.styckepris = styckepris
        self.lagersaldo = lagersaldo
        self.antal_i_korg = 0
        self.totalt_i_korg = 0
    
    def till_dict(self) -> dict:
        """
        Metoden returnerar en dict med varukod, namn, styckepris och lagersaldo,
        eftersom vi inte vill ha med antal_i_korg och totalt_i_korg i filen.
        Metoden används för att spara varorna mellan körningar.
        :return: dictionary med varukod, namn, styckepris och lagersaldo
        """
        return {
            'varukod': self.varukod,
            'namn': self.namn,
            'styckepris': self.styckepris,
            'lagersaldo': self.lagersaldo
        }

    def __str__(self) -> str:
        """
        Metoden returnerar en sträng med varukod, namn, styckepris och lagersaldo.
        Strängen är formaterad så att den passar i tabellen.
        """
        return "{:<6} {:<20} {:>15.2f} {:>10}".format(self.varukod, self.namn, self.styckepris, self.lagersaldo)
    
    def __repr__(self) -> str:
        """
        Metoden returnerar en sträng med information om instansen.
        """
        return f"En instans av {self.__class__.__name__} {self.varukod} {self.namn} {self.styckepris} {self.lagersaldo}"
    
    def __eq__(self, other) -> bool:
        """
        Metoden jämför om två varor är lika.
        """
        if isinstance(other, Vara):
            return self.varukod == other.varukod
        return False


class Varukorg():
    """
    Klassen Varukorg har attributen varor och totalpris.
    Klassen har metoder för att lägga till en vara i varukorgen,
    ta bort en vara ur varukorgen och beräkna totalpriset för varukorgen.
    """
   
    def __init__(self):
        """
        Konstruktorn skapar en tom lista för varorna och sätter totalpris till 0.
        Konstruktorn ger också varukorgen ett id.
        """
        self.varor = []
        self.totalpris = 0
      
    def __str__(self) -> str:
        """
        Metoden returnerar en sträng med varor och totalpris.
        """
        return f"{self.varor} {self.totalpris}"
    
    def __repr__(self) -> str:
        """
        Metoden returnerar en sträng med info om instansen (för testning).
        """
        return f"En instans av {self.__class__.__name__} {self.varor} {self.totalpris}"
    
    def lagg_i_varukorg(self, vara: Vara, antal: int) -> bool:
        """
        Metoden tar emot en vara.
        Om lagersaldot är tillräckligt för önskat antal läggs varan till i varukorgen,
        lagersaldot minskas med samma mängd, och metoden returnerar True.
        Annars returneras False.
        :param vara: Vara
        :param antal: int
        :return: True om lagersaldot ok, annars False
        """
        if vara.lagersaldo >= antal:
            vara.lagersaldo -= antal
            for v in self.varor:
                if v.varukod == vara.varukod:
                    v.antal_i_korg += antal
                    v.totalt_i_korg += v.styckepris * antal
                    self.totalpris += v.styckepris * antal
                    return True
                #else:
            vara.antal_i_korg += antal
            vara.totalt_i_korg += vara.styckepris * antal
            self.varor.append(vara)
            self.totalpris += vara.styckepris * antal
            return True
        else:
            return False

    def ta_bort_vara(self, varukod: str, antal: int) -> bool: 
        """
        Metoden tar emot en vara och tar bort det antal som användaren väljer från varukorgen.
        Lagersaldot ökar med samma antal.
        :param varukod: str
        :param antal: int
        :return: True om tillräckligt av varan finns i varukorgen, annars False
        """    
        for v in self.varor:
            if v.varukod == varukod:
                if v.antal_i_korg < antal:
                    return False
                v.antal_i_korg -= antal
                v.lagersaldo += antal
                v.totalt_i_korg -= v.styckepris * antal
                self.totalpris -= v.styckepris * antal
                if v.antal_i_korg == 0:
                    self.varor.remove(v)
                return True
        return False
    
    def printa_varukorg(self, slutkvitto: bool) -> None:
        """
        Metoden skriver ut varukorgen.
        Rubriken avgörs av om det är ett slutkvitto eller inte.
        :param slutkvitto: True om slutkvitto, annars False
        :return: None
        """
        totalt_antal = 0
        print()
        if slutkvitto:
            print("Kvitto:")
        else:
            print("Varukorg:")
        print("{:<20} {:>7} {:>15} {:>15}".format("Varunamn", "Antal", "A-pris", "Summa"))
        print(64 * "_")
        for vara in self.varor:
            totalt_antal += vara.antal_i_korg
            print(f"{vara.namn:<20} {vara.antal_i_korg:>7} {vara.styckepris:>15.2f} {vara.totalt_i_korg:>15.2f} kr")
        print(64 * "=")
        print(f"Totalt: {totalt_antal:>20}  {self.totalpris:>30.2f} kr")

def las_in_varor(filnamn: str) -> list:
    """
    Funktionen läser in varor från en textfil i JSON-format.
    Varorna läggs till i en lista av instanser av klassen Vara.
    :param filnamn: en sträng med filnamn
    :return: varorna i en lista
    """
    varor = []
    with open(filnamn, 'r') as fil:
        varudatabas = json.load(fil)
        for vara in varudatabas:
            varor.append(Vara(**vara))
    return varor

def printa_varor(varor: list) -> None:
    """
    Funktionen skriver ut varorna som finns i varudatabasen.
    :param varor: varorna
    """
    print("\nTillgängliga varor:")
    print("{:<6} {:<20} {:>15} {:>10}".format("Kod", "Namn", "Pris", "Lagersaldo"))
    varor.sort(key=lambda vara: vara.namn)
    for vara in varor:
        print(vara)

def printa_anvisningar() -> None:
    """
    Funktionen skriver ut anvisningar för användaren.
    """
    print("Ange varukod och antal, t ex '123 2' för att lägga 2 st av varan med varukod 123 i varukorgen.")
    print("Ange varukod och negativt antal tec. '123 -1' för att ta bort en vara ur varukorgen.")
    print("Ange '#' för att skriva ut ett preliminärt kvitto.")
    print("Ange 'j' för att bekräfta köpet.")
    print("Ange 'k' för att skriva ut varukorgen.")
    print("Ange 'v' för att visa listan med varor.")
    print("Ange 'h' för att visa anvisningarna.")
   
def hamta_filnamn() -> str:
    """
    Funktionen frågar efter filnamn och returnerar filnamnet.
    Om filnamnet inte finns, frågar funktionen efter filnamnet igen.
    Användaren kan avbryta programmet genom att ange '#'.
    :return: filnamn
    """
    filnamn = input("Ange filnamn eller '#' för att stänga: ")
    while not os.path.isfile(filnamn) and filnamn != '#':
        filnamn = input("Hittar inte filen. Försök igen: ")
        if filnamn == '#':
            break
    return filnamn

def hantera_varukorg(varukorg: Varukorg, varor: list, inmatning: str) -> None:
    """
    Funktionen tar emot en varukorg, varorna och inmatningen.
    Om antalet varor är positvt, anropas metoden lagg_i_varukorg.
    Om antalet varor är negativt, anropas metoden ta_bort_vara.
    Om varukoden inte finns, skrivs "Varukoden finns inte." ut.
    :param varukorg: varukorgen, en instans av klassen Varukorg
    :param varor: varorna, en lista av instanser av klassen Vara
    :param inmatning: inmatningen, en sträng
    :return: None
    """
    varukod, antal = inmatning.split()
    antal = int(antal)
    kod_finns = False #Utgår från att varukoden inte existerar.
    for vara in varor:
        if vara.varukod == varukod:
            kod_finns = True # Varukoden finns.
            if antal < 0:
                if varukorg.ta_bort_vara(varukod, abs(antal)):
                    print(f"{abs(antal)} {vara.namn} togs bort från varukorgen.")
                else:
                    print("Du kan inte ta bort fler varor än vad som finns i varukorgen.")
                continue
            else:    
                if varukorg.lagg_i_varukorg(vara, antal):
                    print(f"{antal} {vara.namn} {vara.styckepris} kr/st lades till i varukorgen.")
                else:
                    print("Varan finns inte i lager.")
                    continue
    if not kod_finns:    
        print("Varukoden finns inte.")
    
    return

def huvudslingan(varor: list) -> None:
    """
    Funktionen är huvudslingan i programmet.
    Här finns en while-loop som frågar efter varukod och antal.
    Inmatningen kollas mot ett regex-mönster.
    Om inmatningen matchar regex anropas hantera_varukorg().
    Om inmatningen är '#', skrivs varukorgen ut och användaren får frågan om den vill bekräfta köpet.
    Om inmatningen är 'k', skrivs varukorgen ut.
    Om inmatningen är 'v', skrivs varorna ut.
    Om inmatningen är 'h', skrivs anvisningarna ut.
    Om inmatningen inte matchar nåt av ovanstående "Felaktig inmatning. Försök igen." ut.
    :param varor: varorna, en lista av instanser av klassen Vara
    :return: None
    """
    varukorg = Varukorg()
    while True:
        inmatning = input("Ange varukod och antal (eller kommando): ")
        if re.match(regex_inmatning, inmatning):
            hantera_varukorg(varukorg, varor, inmatning)
            continue
        elif inmatning == '#':
            varukorg.printa_varukorg(False)
            inmatning = input("Vill du bekräfta köpet? (j = Ja): ")
            if inmatning.lower() == 'j':
                varukorg.printa_varukorg(True)
                break
            else:
                continue
        elif inmatning == 'k':
            varukorg.printa_varukorg(False)
            continue
        elif inmatning == 'v':
            printa_varor(varor)
            continue
        elif inmatning == 'h':
            printa_anvisningar()
            continue
        else:
            print("Felaktig inmatning. Försök igen.")
            continue

def spara_och_avsluta(varor: list, filnamn: str)-> None:
        """
        Metoden sparar varorna till en textfil i JSON-format och avslutar programmet.
        :param varor: varorna, en lista av instanser av klassen Vara
        :param filnamn: filnamnet för textfilen
        :return: None
        """
        varuinstanser = [vara.till_dict() for vara in varor]
        with open(filnamn, 'w', encoding='utf-8') as file:
            json.dump(varuinstanser, file, indent=4, ensure_ascii=False)

def main():
    """
    Huvudprogrammet.
    Hälsa välkommen och skriv ut anvisningar.
    Fråga efter filnamn och läs in varorna.
    Skapa en varukorg.
    """
    print("Välkommen till kassakonsolen!")
    printa_anvisningar()
    filnamn = hamta_filnamn()
    if filnamn == '#':
        print("Hej då!")
        return
    else:
        varor = las_in_varor(filnamn)
        printa_varor(varor)
        huvudslingan(varor)
        spara_och_avsluta(varor, filnamn)

if __name__ == '__main__':
    main()
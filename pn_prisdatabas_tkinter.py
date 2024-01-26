"""
DD100V Assignment p-uppgift
Uppgift: 145 Varuprisdatabas
Student: Peter Nyström
Datum: 10 januari, 2024
Detta program hanterar en varuprisdatabas.
Varje produkt har en varukod, ett namn, ett styckepris och ett lagersaldo.
Programmet läser in varor från en textfil i JSON-format.
Produkterna läses in till en lista av instaser av klassen Vara.
Datastrukturen för varukorgen ser ut så här:
varukorg = [
    {'varukod': '123', 'namn': 'Banan', 'styckepris': 10.0, 'antal': 2, 'totalt': 20.00},
    {'varukod': '456', 'namn': 'Äpple', 'styckepris': 5.0, 'antal': 1, 'totalt': 5.00},
    {'varukod': '789', 'namn': 'Apelsin', 'styckepris': 7.5, 'antal': 3, 'totalt': 22.50}
    ]
Datastrukturen för varorna ser ut så här:
varor = [
    {'varukod': '123', 'namn': 'Banan', 'styckepris': 10.0, 'lagersaldo': 100},
    {'varukod': '456', 'namn': 'Äpple', 'styckepris': 5.0, 'lagersaldo': 50},
    {'varukod': '789', 'namn': 'Apelsin', 'styckepris': 7.5, 'lagersaldo': 200}
    ]

"""
import json # behövs för att läsa och skriva JSON-filer
import os # behövs för att kontrollera om filen finns

from tkinter import Tk, Label, Button, Entry, StringVar # behövs för GUI
from tkinter import ttk # behövs för GUI

#Vi använder en parameter för filnamnet så att vi kan ändra det om vi vill
VARUDATABAS = "fler_varor.txt"

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
        """
        return f"{self.varukod} {self.namn} {self.styckepris} {self.lagersaldo}"
    
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
    
    def lagg_i_varukorg(self, vara: Vara) -> bool:
        """
        Metoden tar emot en vara.
        Om lagersaldot är > 1 läggs varan till i varukorgen, lagersaldot minskas med 1
        och metoden returnerar True.
        Annars returneras False.
        :param vara: Vara.varukod
        :return: True om lagersaldot är > 1, annars False
        """
        if vara.lagersaldo >= 1:
            vara.lagersaldo -= 1
            for v in self.varor:
                if v.varukod == vara.varukod:
                    v.antal_i_korg += 1
                    v.totalt_i_korg += v.styckepris
                    break
            else:
                vara.antal_i_korg += 1
                vara.totalt_i_korg += vara.styckepris
                self.varor.append(vara)
                self.totalpris += vara.styckepris
            return True
        else:
            return False

    def ta_bort_vara(self, varukod: str) -> list: 
        """
        Metoden tar emot en vara och tar bort den från varukorgen.
        Lagersaldot ökar med det antal som fanns i varukorgen.
        :param vara: Vara.varukod
        :return: varukorgen
        """    
        for v in self.varor:
            if v.varukod == varukod:
                v.antal_i_korg -= 1
                v.lagersaldo += 1
                v.totalt_i_korg -= v.styckepris 
                self.totalpris -= v.styckepris
                if v.antal_i_korg == 0:
                    self.varor.remove(v)
                break
        return self.varor
       
    def berakna_totalpris(self) -> float:
        """ 
        Metoden beräknar totalpriset för varukorgen genom att loopa igenom
        varorna i korgen. 
        :param: varukorg (ie self)
        :return: totalpriset för varukorgen
        """
        #Beräkna totalpriset för varukorgen
        #Returnera totalpriset för varukorgen
        # loopa igenom varukorgen
        # för varje vara i varukorgen, lägg till styckepris till totalpriset
        # returnera totalpriset
        self.totalpris = 0
        for vara in self.varor:
            self.totalpris += vara.totalt_i_korg
        return self.totalpris  
    

class App:
    """
    Denna klass skapar ett GUI för ett kassasystem.
    Här finns metoder för att:
    *få en meny med varor 
    *lägga en vara i varukorgen genom att dubbelklicka på varan i varulistan
    *ta bort en vara ur varukorgen genom att dubbelklicka på varan
    *visa varukorgen sorterad efter varunamn med 
    kolumnerna namn, styckepris, antal och totalt pris

    GUI har två ramar, en för varukorgen och en för varorna.
    Varorna visas i en ttk.Treeview där man dubbelklickar på varje vara så att den läggs i varukorgen.
    Varukorgen visas i det vänstra fönstret.
    Varukorgen visas med kolumnerna namn, styckepris, antal och totalt pris.
    Varukorgen är sorterad efter varunamn.
    Längst ned finns totala summan av varukorgen.
    Under varukorgen finns en knapp för att betala. 
    Det finns en knapp för att avsluta programmet. Innan programmet avslutas
    sparas varorna till en textfil i JSON-format med aktuella lagersaldon.
    """
    def __init__(self, root, varor: list):
        """
        :param root: Tkinter-instans
        :param varor: lista med varor, dvs en lista med instanser av klassen Vara
        """
        self.root = root
        self.varor = varor
        self.root.title("Kassasystem")
        self.varukorg = Varukorg()
        
        # Anropa metoden som skapar GUI-element
        self.skapa_gui_element()

        #self.skapa_meny()
        self.bind_tree_varor_event(varor)
   
        self.skapa_varor(self.varor)
        #self.main_frame.pack()
        self.main_frame.pack(fill='both', expand=True)
        self.root.mainloop()

    def bind_tree_varor_event(self, varor: list)-> None:
        """
        Metoden binder ett event (dubbelklick) till treeview för varorna.
        :param varor: listan med varor
        :return: None
        """
        self.tree_varor.bind('<Double-1>', lambda event: self.on_double_click(event, 
                                            varor[self.tree_varor.index(self.tree_varor.selection()[0])]))

    def on_double_click(self, event, vara: Vara)-> None:
        """
        Tar emot ett event och en vara efter ett dubbelklick på en vara i treeview för varorna.
        Lägger till varan i varukorgen och uppdaterar varukorgen.
        :param event: eventet som skickas med (används dock inte)
        :param item: varan som klickats på
        :return: None
        """
        if vara:
            vara_finns_i_lager = self.varukorg.lagg_i_varukorg(vara)
            if not vara_finns_i_lager:
                # Visa en inforuta om att varan inte finns i lager
                self.visa_varan_slut(vara.namn)
            else:
                self.uppdatera_varukorg(self.varukorg.varor)
                # Updatera lagersaldo i treeview för varorna
                selected_item = self.tree_varor.selection()[0]
                self.tree_varor.set(selected_item, '#3', vara.lagersaldo)

    def visa_varan_slut(self, vara: str)->None:
        """
        Metoden används för att meddela att varan är slut på lagret
        :param vara: en sträng med namnet på varan som är slut
        :return None:
        """
        meddelande = Tk()
        meddelande.title("Vara slut i lager")

        # Texten
        tomma_raden = Label(meddelande, text = "")
        tomma_raden.pack()
        meddelande_text = Label(meddelande, text=f"Ursäkta oss, men {vara} är slut på lagret.")
        meddelande_text.pack()

        # Knappen
        ok_knapp = Button(meddelande, text="OK", command=meddelande.destroy)
        ok_knapp.pack()

        # Placera meddelandet mitt på skärmen
        meddelande.update_idletasks()
        width = meddelande.winfo_width()
        padding = 20  # Skapa lite luft 
        width += 2 * padding
        height = 4 * padding
        x = (meddelande.winfo_screenwidth() // 2) - (width // 2)
        y = (meddelande.winfo_screenheight() // 2) - (height // 2)
        meddelande.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        meddelande.mainloop()

    def skapa_varor(self, varor: list):
        """
        Metoden skapar en ttk.Treeview för varorna och fyller den med innehållet från varor-parametern.
        :param varor: listan med varor, dvs en lista med instanser av klassen Vara
        :return: None
        """
        # Rensa först bort alla varor i varukorgen
        for item in self.tree_varor.get_children():
            self.tree_varor.delete(item)

        varor.sort(key=lambda vara: vara.namn)  # Sortera varorna efter namn
        # Skapa en Treeview-widget för tabellayout
        for vara in varor:
            varuinfo = (
                vara.varukod,
                f"{vara.styckepris:.2f}",  # Avruna till två decimaler
                vara.lagersaldo
            )
            self.tree_varor.insert('', 'end', text=vara.namn, values=varuinfo)
            
        # Sätt individuella kolumnbredder, samma alignment som för kolumnrubrikerna
        self.tree_varor.column('#0', width=150)  
        self.tree_varor.column('#1', width=100, anchor='e')
        self.tree_varor.column('#2', width=100, anchor='e')
        self.tree_varor.column('#3', width=100, anchor='center')
        self.tree_varor.pack(fill='both', expand=True)

    def rensa_vara(self, event)-> None:
        """
        Metoden tar bort en vara ur varukorgen och uppdaterar denna.
        :param event: eventet som skickas med (används dock inte)
        :return: None
        """
        if not self.tree.selection():
            return
        item_id = self.tree.selection()[0]
        selected_item = self.tree.item(item_id)

        if selected_item:
            varukod = selected_item['tags'][0].split(' ')[0]  # Hämta varukoden från taggen
            varukorg = self.varukorg.ta_bort_vara(varukod)

        # Uppdatera varukorgen
        self.uppdatera_varukorg(varukorg)
        self.skapa_varor(self.varor)

    
    def uppdatera_varukorg(self, varor: list())-> None:
        """
        Uppdaterar varukorgen med de varor som finns i varukorgen.
        :param items: varorna i varukorgen
        :return: None
        """
        # Rensa först bort alla varor i varukorgen
        self.tree.delete(*self.tree.get_children())

        # När varorna läggs in i treeview räknar vi ut totalpriset också
        totalpris = 0
        varor.sort(key=lambda vara: vara.namn)  # Sortera varorna efter namn
        # Infoga varorna i varukorgen i treeview
        for vara in varor:
            varudata = (
                f"{vara.styckepris:.2f}",  # Avrunda till två decimaler   
                vara.antal_i_korg,
                f"{vara.totalt_i_korg:.2f}",  # Avrunda till två decimaler
            )
            self.tree.insert('', 'end', text=vara.namn, values=varudata, tags=(vara,))
            totalpris += vara.totalt_i_korg

        # Uppdatera totalpriset
        self.totalpris.config(text=f"Totalt: {totalpris:.2f} kr")
       

    def skapa_gui_element(self)-> None:
        """
        Metoden skapar GUI-element, knappar, rubriker.
        :return: None
        """
         # Skapa ett förnster med en ram för varukorgen och en för varorna
        self.main_frame = ttk.Frame(self.root)
        self.varukorg_frame = ttk.LabelFrame(self.main_frame, text="Varukorg")
        self.varor_frame = ttk.LabelFrame(self.main_frame, text="Varor")
        self.varukorg_frame.pack(side="left", fill="both", expand=True)
        self.varor_frame.pack(side="right", fill="both", expand=True)

        self.tree = ttk.Treeview(self.varukorg_frame, columns=('Styckepris', 'Antal', 'Totalt'))
        self.tree.heading('#0', text='Namn', anchor='w')
        self.tree.heading('#1', text='Styckepris', anchor='e')
        self.tree.heading('#2', text='Antal', anchor='e')
        self.tree.heading('#3', text='Totalt', anchor='center')

        self.tree.column('#0', width=150, anchor='w')  
        self.tree.column('#1', width=100, anchor='e')  
        self.tree.column('#2', width=100, anchor='e')  
        self.tree.column('#3', width=100, anchor='e')  
        self.tree.pack(fill='both', expand=True)
        self.tree.bind('<Double-1>', self.rensa_vara)

        self.tree_varor = ttk.Treeview(self.varor_frame, columns=('Varukod', 'Styckepris', 'Lagersaldo'))  
        self.tree_varor.heading('#0', text='Namn')
        self.tree_varor.heading('#1', text='Varukod')
        self.tree_varor.heading('#2', text='Styckepris')
        self.tree_varor.heading('#3', text='Lagersaldo')
        self.tree_varor.pack(fill='both', expand=True)
        
        self.totalpris = ttk.Label(self.varukorg_frame, text=f"Totalt: {self.varukorg.berakna_totalpris():.2f} kr")
        self.totalpris.pack()
        
        # Lägg in en knapp för att betala
        self.betala = ttk.Button(self.varukorg_frame, text="Betala", command=self.betala)
        self.betala.pack()
        
        # Lägg in en knapp för att avsluta programmet
        self.quit_button = ttk.Button(self.varor_frame, text="Avsluta", command= lambda: self.spara_och_avsluta(VARUDATABAS))
        self.quit_button.pack()
        
    def betala(self) -> None:
        """
        Metoden skapar ett kvittofönster med en egen Treeview-widget för tabellayout.
        """
        # Skapa ett kvittofönster
        kvitto_window = Tk()
        kvitto_window.title("Kvitto")

        # Skapa en Treeview-widget för tabellayout
        tree = ttk.Treeview(kvitto_window, columns=('Styckepris', 'Antal', 'Totalt'))
        tree.heading('#0', text='Produkt', anchor='w')
        tree.heading('#1', text='Styckepris', anchor='center')
        tree.heading('#2', text='Antal', anchor='center')
        tree.heading('#3', text='Totalt', anchor='e')
        
        # Lägg till varor i tabellen
        for vara in self.varukorg.varor:
            varuinfo = (
                f"{vara.styckepris:.2f}",  # Avrunda till två decimaler   
                vara.antal_i_korg,
                f"{vara.totalt_i_korg:.2f}",  # Avrunda till två decimaler
            )
            tree.insert("", "end",text=vara.namn, values=varuinfo)

        # Sätt individuella kolumnbredder, samma alignment som för kolumnrubrikerna
        tree.column('#0', width=150, anchor='w')  
        tree.column('#1', width=100, anchor='center')  
        tree.column('#2', width=100, anchor='center')  
        tree.column('#3', width=100, anchor='e')  
        tree.pack()

        # Lägg in totalen
        tree.insert("", "end", values=("","","","")) # Först en tom rad
        total_value = self.varukorg.totalpris
        total_row = ("Totalt", f"{total_value:.2f} kr", "", "" )
        tree.insert("", "end", values=total_row, tags=("total",)) 
        tree.tag_configure("total", font="Helvetica 12 bold", background="lightgrey", foreground="black")

        tack_label = Label(kvitto_window, text="Tack för ditt köp!")
        tack_label.pack()

        # Skapa en knapp för att rensa varukorgen och skapa en ny varukorg
        rensa_knapp = Button(kvitto_window, text="Nästa kund", command=lambda: [self.rensa_varukorg(), kvitto_window.destroy()])
        rensa_knapp.pack()

        # Lägg kvittofönstret i mitten av skärmen
        kvitto_window.update_idletasks()
        width = kvitto_window.winfo_width()
        height = kvitto_window.winfo_height()
        x = (kvitto_window.winfo_screenwidth() // 2) - (width // 2)
        y = (kvitto_window.winfo_screenheight() // 2) - (height // 2)
        kvitto_window.geometry(f"450x{height}+{x}+{y}")

        # Starta event loop
        kvitto_window.mainloop()  

    def rensa_varukorg(self)-> None:
        """
        Metoden rensar varukorgen genom att skapa en ny varukorg.
        Metoden kallas när man klickar på knappen "Nästa kund" i kvittot.
        :return: None
        """
        self.varukorg = Varukorg()
        self.uppdatera_varukorg([])

    def spara_och_avsluta(self, filnamn: str)-> None:
        """
        Metoden sparar varorna till en textfil i JSON-format och avslutar programmet.
        :param filnamn: filnamnet för textfilen
        :return: None
        """
        varuinstanser = [vara.till_dict() for vara in self.varor]
        with open(filnamn, 'w', encoding='utf-8') as file:
            json.dump(varuinstanser, file, indent=4, ensure_ascii=False)
        # När aktuellt lager är sparat så avslutas programmet
        self.root.destroy()

def varor_fran_fil(filnamn: str)-> list:
    """
    Metoden läser in varorna från en textfil i JSON-format.
    Metoden returnerar en lista med instanser av klassen Vara.
    Notera att filnamnet är en parameter så vi bryr oss inte om felhantering här.
    :param file_name: filnamnet för textfilen
    :return: en lista med instanser av klassen Vara
    """
    vara_instances = []
    with open(filnamn, 'r') as file:
        varor = json.load(file)
        for item in varor:
            vara_instance = Vara(item['varukod'], item['namn'], item['styckepris'], item['lagersaldo'])
            vara_instances.append(vara_instance)
    return vara_instances

def visa_anvisningar()-> None:
    """
    Metoden visar instruktioner för användaren.
    När man klickar på OK så stängs fönstret och programmet fortsätter genom att
    skapa en instans av klassen App som startar kassaappen.
    :return: None
    """
    # Tkinter fönster för instruktioner
    anvisningar = Tk()
    anvisningar.title("145 Varuprisdatabas")
    # Instruktionstexten
    anvisning_text = Label(anvisningar, text="""
        Välkommen till kassasystemet!
    
        När du klickar på OK så läser programmet in alla varor från databasen.
        För att lägga en vara i varukorgen så dubbelklickar du på varan i listan.
                              
        För att ta bort en vara ur varukorgen så dubbelklickar du på varan i varukorgen.
        För att betala så klickar du på knappen Betala, då kommer ett kvitto och varukorgen rensas.
                           
        För att avsluta programmet så klickar du på knappen Avsluta. Då sparas också
        varorna till databasen.
                           
    """)
    anvisning_text.pack()

    # OK-knappen
    fattar_knapp = Button(anvisningar, text="OK", command=anvisningar.destroy)
    fattar_knapp.pack()

    # Lägg instruktionsfönstret i mitten av skärmen
    anvisningar.update_idletasks()
    bredd = anvisningar.winfo_width()
    hojd = anvisningar.winfo_height()
    padding = 20  # Skapa lite luft runt texten
    bredd += 2 * padding
    hojd += 2 * padding
    x = (anvisningar.winfo_screenwidth() // 2) - (bredd // 2)
    y = (anvisningar.winfo_screenheight() // 2) - (hojd // 2)
    anvisningar.geometry('{}x{}+{}+{}'.format(bredd, hojd, x, y))
    
    anvisningar.mainloop()

def hamta_filnamn()-> str:
    """
    Metoden returnerar filnamnet för varudatabasen.
    Funktionen ger ett default-värde som är filnamnet för den databas som används i uppgiften.
    :return: filnamnet för varudatabasen
    """
    def kolla_filnamn():
        filnamn = inmatning.get()
        if os.path.isfile(filnamn):
            filnamn_str.set(filnamn)
            root.destroy()
        else:
            ruta.config(text="Filen finns inte. Försök igen.")

    root = Tk()
    root.title("Ange sökväg/filnamn för varudatabasen")

    ruta = Label(root, text="Ange sökväg/filnamn för varudatabasen:")
    ruta.pack()

    inmatning = Entry(root)
    inmatning.insert(0, VARUDATABAS)
    inmatning.pack()

    filnamn_str = StringVar()

    knapp = Button(root, text="OK", command=lambda: kolla_filnamn())
    knapp.pack()

    root.bind('<Return>', lambda event: kolla_filnamn())

    # Registrera en callback-funktion som anropas när fönstret stängs
    root.protocol("WM_DELETE_WINDOW", root.destroy)

    # Placera fönstret mitt på skärmen
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)

    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    root.wait_window(root)

    return filnamn_str.get()

def main():
    """
    Huvudprogrammet frågar efter sökvägen med filen som innehåller varudatabasen
    varefter vi läser in varorna från en textfil i JSON-format.
    Sedan anropas en funktion som visar instruktioner för användaren.
    Därefter skapas en instans av tkinter (Tk) och en instans av klassen App.
    När App-instansen skapas skickas Tk-instansen och varorna med som parametrar
    och kassaappen startar.
    """
    filnamn = hamta_filnamn()
    #läs in varor från databasen, en json-fil
    varor = varor_fran_fil(filnamn)
    visa_anvisningar()
    root = Tk()
    app = App(root, varor)
 
if __name__ == "__main__":
    main()


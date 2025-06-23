from tkinter import * #Importuje wszystkie klasy i funkcje z biblioteki tkinter, służącej do tworzenia GUI w Pythonie.
import tkintermapview #Importuje bibliotekę tkintermapview

#Tworzy trzy puste listy do przechowywania danych o hotelach, klientach i pracownikach.
hotels:list=[]
clients:list=[]
workers:list=[]

class Hotels: #Definicja klasy Hotels — przechowuje informacje o hotelach.
  def __init__(self, hotel_name, hotel_location):
  # Konstruktor - Przyjmuje nazwę i lokalizację hotelu.
   self.hotel_name = hotel_name #Zapisuje parametry jako atrybuty obiektu
   self.hotel_location = hotel_location #Zapisuje parametry jako atrybuty obiektu
   self.coordinates = self.get_coordinates() #Pobiera współrzędne lokalizacji (z Wikipedii).
   # self.marker=map_widget.set_marker(self.coordinates[0],self.coordinates[1])

def add_hotel():
 #wprowadzanie danych hotelu
  hotel_nazwa = entry_name.get() #Pobiera dane z pól formularza GUI.
  hotel_miejscowosc = entry_location.get() #Pobiera dane z pól formularza GUI.
  hotel_lat = entry_lat.get() #Pobiera dane z pól formularza GUI.
  hotel_long = entry_long.get() #Pobiera dane z pól formularza GUI.
  category = category_var.get()

  if category == "Hotel":
     hotel = {"name": name, "location": location, "lat": "0", "long": "0"}
     hotels.append(hotel)
     listbox_hotels.insert(END, f"{name} - {location}")

  elif category == "Pracownik":
    worker = {"name": name, "surname": surname, "hotel": location}
    workers.append(worker)
    listbox_workers.insert(END, f"{name} {surname} - {location}")

  elif category == "Gosc":
    client = {"name": name, "surname": surname, "hotel": location}
    clients.append(client)
    listbox_clients.insert(END, f"{name} {surname} - {location}")

    hotel = {'name': hotel_nazwa, 'location': hotel_miejscowosc, 'lat': hotel_lat, 'long': hotel_long}
    hotels.append(hotel) #Tworzy słownik z danymi hotelu i dodaje go do listy hotels

 #opcje usuwania informacji - Czyści pola tekstowe po dodaniu hotelu.
    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_lat.delete(0, END)
    entry_long.delete(0, END)

    #Ustawia fokus i odświeża listę oraz markery na mapie.
    entry_name.focus()
    map_widget.delete_all_marker()
    show_hotels()

    def get_coordinates(self) -> list: #Metoda pobierająca współrzędne lokalizacji hotelu z Wikipedii.
        import requests
        from bs4 import BeautifulSoup #Importuje biblioteki do pobierania i parsowania HTML.
        url = f"https://pl.wikipedia.org/wiki/{self.hotel_location}" #Tworzy URL do strony Wikipedii i pobiera HTML.
        response = requests.get(url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        print(longitude) #Zwraca współrzędne jako listę.
        print(latitude) #Zwraca współrzędne jako listę.
        return [latitude, longitude] #Zwraca współrzędne jako listę.


def show_hotels(): #Zwraca współrzędne jako listę.
    listbox_lista_hoteli.delete(0,END) #czyści listbox
    for idx,hotel in enumerate(hotels): #iteruje przez listę hotels
        listbox_lista_hoteli.insert(idx,f'{idx+1}. {hotel['name']} - {hotel['location']} ({hotel['lat']} {hotel['long']})')
        map_widget.set_marker(float(hotel['lat']), float(hotel['long']),
                              text=f"{hotel['name']}",
                              text_color="purple",  # Kolor Textu nad markerem
                              marker_color_circle="purple",  # Kolor kółka markera
                              marker_color_outside="orange", # Kolor zewnętrznej obwódki markera
                              font=("Times New Roman", 6, "bold"))

def remove_hotel():
    i=listbox_lista_hoteli.index(ACTIVE)
    hotels.pop(i)
    show_hotels()

def edit_hotel():
    i=listbox_lista_hoteli.index(ACTIVE) #Edytuje wybrany hotel — dane trafiają do formularza.
    name=hotels[i]['name']
    location=hotels[i]['location']
    lat=hotels[i]['lat']
    long=hotels[i]['long']

    entry_name.insert(0,name)
    entry_location.insert(0,location)
    entry_lat.insert(0,lat)
    entry_long.insert(0,long)

    button_dodaj_obiekt.config(text="Zapisz", command=lambda: update_hotels(i))


def update_hotels(i): #Aktualizuje dane hotelu w liście hotels na podstawie formularza.
    new_name=entry_name.get()
    new_location=entry_location.get()
    new_lat=entry_lat.get()
    new_long=entry_long.get()

    hotels[i]['name']=new_name
    hotels[i]['location']=new_location
    hotels[i]['lat']=new_lat
    hotels[i]['long']=new_long

    entry_name.delete(0,END)
    entry_location.delete(0,END)
    entry_lat.delete(0,END)
    entry_long.delete(0,END)
    entry_name.focus()

    button_dodaj_obiekt.config(text="Dodaj hotel", command=add_hotel)
    show_hotels()

class Client:
    def __init__(self,client_name,client_hotel,client_location1,client_location2):
        self.client_name =client_name
        self.client_hotel=client_hotel
        self.client_location1=client_location1
        self.client_location2=client_location2
        self.coordinates=self.get_coordinates()
        # self.marker=map_widget.set_marker(self.coordinates[0],self.coordinates[1])

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{self.client_location2}"
        response = requests.get(url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        print(longitude)
        print(latitude)
        return [latitude, longitude]


class Workers:
    def __init__(self,worker_name,worker_hotel,worker_location):
        self.worker_name =worker_name
        self.worker_hotel=worker_hotel
        self.worker_location=worker_location

        self.coordinates=self.get_coordinates()
        # self.marker=map_widget.set_marker(self.coordinates[0],self.coordinates[1])

    def get_coordinates(self) -> list:
        import requests
        from bs4 import BeautifulSoup
        url = f"https://pl.wikipedia.org/wiki/{self.worker_location}"
        response = requests.get(url).text
        response_html = BeautifulSoup(response, "html.parser")
        longitude = float(response_html.select(".longitude")[1].text.replace(",", "."))
        latitude = float(response_html.select(".latitude")[1].text.replace(",", "."))
        print(longitude)
        print(latitude)
        return [latitude, longitude]


#wpisywanie informacji w miejsce "...."
def show_user_details():
    i=listbox_lista_obiektow.index(ACTIVE)
    name=hotels[i]['name']
    location=hotels[i]['location']
    lat=hotels[i]['lat']
    long=hotels[i]['long']
    label_szczegoly_name_wartosc.config(text=name)
    label_szczegoly_location_wartosc.config(text=location)
    label_szczegoly_lat_wartosc.config(text=lat)
    label_szczegoly_long_wartosc.config(text=long)

root = Tk() #Tworzy główne okno aplikacji.
root.geometry("1200x760")
root.title("Map Book MJ")
#Ustawia rozmiar i tytuł.

#Ramki
ramka_lista_obiektow=Frame(root)
ramka_formularz=Frame(root)
ramka_szczegoly_obiektow=Frame(root)
ramka_mapa=Frame(root)
#Tworzy i rozmieszcza ramki dla widżetów GUI.

ramka_lista_obiektow.grid(row=0, column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektow.grid(row=1, column=0,columnspan=2)
ramka_mapa.grid(row=2, column=0, columnspan=2)


# ramka_lista_obiektow
label_lista_obiektow=Label(ramka_lista_obiektow, text="Lista hoteli")
label_lista_obiektow.grid(row=0, column=0,columnspan=2)
listbox_lista_obiektow=Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)
button_pokaz_szczegoly_obiektu=Button(ramka_lista_obiektow, text='Pokaż szczegóły')
button_pokaz_szczegoly_obiektu.grid(row=2, column=0)
button_usun_obiekt=Button(ramka_lista_obiektow, text='Usuń obiekt')
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt=Button(ramka_lista_obiektow, text='Edytuj obiekt')
button_edytuj_obiekt.grid(row=2, column=2)


label_lista_obiektow_klient=Label(ramka_lista_obiektow, text="Lista pracowników")
label_lista_obiektow_klient.grid(row=0, column=3,columnspan=2)
listbox_lista_obiektow_klient=Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_obiektow_klient.grid(row=1, column=3, columnspan=3)
button_pokaz_szczegoly_obiektu_klient=Button(ramka_lista_obiektow, text='Pokaż szczegóły')
button_pokaz_szczegoly_obiektu_klient.grid(row=2, column=3)
button_usun_obiekt_klient=Button(ramka_lista_obiektow, text='Usuń obiekt')
button_usun_obiekt_klient.grid(row=2, column=4)
button_edytuj_obiekt_klient=Button(ramka_lista_obiektow, text='Edytuj obiekt')
button_edytuj_obiekt_klient.grid(row=2, column=5)

label_lista_obiektow_klient=Label(ramka_lista_obiektow, text="Lista klientów")
label_lista_obiektow_klient.grid(row=0, column=6,columnspan=2)
listbox_lista_obiektow_klient=Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_obiektow_klient.grid(row=1, column=6, columnspan=3)
button_pokaz_szczegoly_obiektu_klient=Button(ramka_lista_obiektow, text='Pokaż szczegóły')
button_pokaz_szczegoly_obiektu_klient.grid(row=2, column=6)
button_usun_obiekt_klient=Button(ramka_lista_obiektow, text='Usuń obiekt')
button_usun_obiekt_klient.grid(row=2, column=7)
button_edytuj_obiekt_klient=Button(ramka_lista_obiektow, text='Edytuj obiekt')
button_edytuj_obiekt_klient.grid(row=2, column=8)

# ramka_formularz
label_formularz=Label(ramka_formularz, text="Formularz")
label_formularz.grid(row=0, column=0, columnspan=2)
label_name=Label(ramka_formularz, text="Imię:")
label_name.grid(row=1, column=0, sticky=W)
label_surname=Label(ramka_formularz, text="Nazwisko:")
label_surname.grid(row=2, column=0,sticky=W)
label_location=Label(ramka_formularz, text="Miejscowość:")
label_location.grid(row=3, column=0,sticky=W)
label_posts=Label(ramka_formularz, text="Postów:")
label_posts.grid(row=4, column=0,sticky=W)

entry_name=Entry(ramka_formularz)
entry_name.grid(row=1, column=1)
entry_surname=Entry(ramka_formularz)
entry_surname.grid(row=2, column=1)
entry_location=Entry(ramka_formularz)
entry_location.grid(row=3, column=1)
entry_posts=Entry(ramka_formularz)
entry_posts.grid(row=4, column=1)

button_dodaj_obiekt=Button(ramka_formularz, text='Dodaj hotel')
button_dodaj_obiekt.grid(row=5, column=0, columnspan=2)

button_dodaj_obiekt=Button(ramka_formularz, text='Dodaj klienta')
button_dodaj_obiekt.grid(row=6, column=0, columnspan=2)

button_dodaj_obiekt=Button(ramka_formularz, text='Dodaj pracownika')
button_dodaj_obiekt.grid(row=7, column=0, columnspan=2)

# ramka_szczegoly_obiektow
label_szczegoly_obiektow=Label(ramka_szczegoly_obiektow, text="Szczegoly obiektu:")
label_szczegoly_obiektow.grid(row=0, column=4)
label_szczegoly_name=Label(ramka_szczegoly_obiektow, text="Imię:")
label_szczegoly_name.grid(row=1, column=0)
label_szczegoly_name_wartosc=Label(ramka_szczegoly_obiektow, text="  ...  ")
label_szczegoly_name_wartosc.grid(row=1, column=1)
label_szczegoly_surname=Label(ramka_szczegoly_obiektow, text="Nazwisko:")
label_szczegoly_surname.grid(row=1, column=2)
label_szczegoly_surname_wartosc=Label(ramka_szczegoly_obiektow, text="  ...")
label_szczegoly_surname_wartosc.grid(row=1, column=3)
label_szczegoly_location=Label(ramka_szczegoly_obiektow, text="Miejscowość:")
label_szczegoly_location.grid(row=1, column=4)
label_szczegoly_location_wartosc=Label(ramka_szczegoly_obiektow, text="...  ")
label_szczegoly_location_wartosc.grid(row=1, column=5)
label_szczegoly_posts=Label(ramka_szczegoly_obiektow, text="Posty:")
label_szczegoly_posts.grid(row=1, column=6)
label_szczegoly_posts_wartosc=Label(ramka_szczegoly_obiektow, text="  ...  ")
label_szczegoly_posts_wartosc.grid(row=1, column=7)

# Formularz
Label(ramka_formularz, text="Dodaj wpis").grid(row=0, column=0, columnspan=2)

category_var = StringVar()
category_var.set("Hotel")

OptionMenu(ramka_formularz, category_var, "Hotel", "Pracownik", "Gosc").grid(row=1, column=0, columnspan=2)

Label(ramka_formularz, text="Imie / Nazwa").grid(row=2, column=0, sticky=W)
entry_name = Entry(ramka_formularz)
entry_name.grid(row=2, column=1)

Label(ramka_formularz, text="Nazwisko").grid(row=3, column=0, sticky=W)
entry_surname = Entry(ramka_formularz)
entry_surname.grid(row=3, column=1)

Label(ramka_formularz, text="Miejscowosc / Hotel").grid(row=4, column=0, sticky=W)
entry_location = Entry(ramka_formularz)
entry_location.grid(row=4, column=1)

Button(ramka_formularz, text="Dodaj", command=add_entry).grid(row=5, column=0, columnspan=2, pady=10)


# ramka_mapa
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=500, corner_radius=5)
map_widget.grid(row=0, column=0, columnspan=2)
map_widget.set_position(52.23,21.0)
map_widget.set_zoom(6)
#Inicjalizuje mapę na Warszawie z domyślnym zoomem.



root.mainloop() #Uruchamia pętlę zdarzeń aplikacji tkinter.
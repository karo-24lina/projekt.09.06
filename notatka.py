#<<<<<<< 
feat-init-data
print('Hello world')
#=======
from tkinter import *
from tkinter import ttk  # Import ttk for Treeview and Notebook
import tkintermapview
from tkinter import messagebox  # For confirmation dialogs

hotels: list = []
workers: list = []

#=--------------------------------------HOTELE---------------------------------------------=
def load_default_hotels():
    map_widget.delete_all_marker()  # Usuń wszystkie markery, aby narysować od nowa
    show_hotels()  # Odśwież widok hoteli i mapę

def add_hotel():
    hotel_nazwa = entry_name.get().strip()
    hotel_miejscowosc = entry_location.get().strip()
    hotel_lat_str = entry_lat.get().strip()
    hotel_long_str = entry_long.get().strip()

    try:
        hotel_lat = float(hotel_lat_str)
        hotel_long = float(hotel_long_str)
    except ValueError:
        messagebox.showerror("Błąd danych", "Kliknij na mapie by wybrac Polozenie hotelu")
        return

        return

    hotel = {'name': hotel_nazwa, 'location': hotel_miejscowosc, 'lat': hotel_lat, 'long': hotel_long}
    hotels.append(hotel)

    clear_form_entries()
    entry_name.focus()

    map_widget.delete_all_marker()
    show_hotels()


def show_hotels():
    for i in treeview_lista_obiektow.get_children():
        treeview_lista_obiektow.delete(i)

    map_widget.delete_all_marker()

    for idx, hotel in enumerate(hotels):
        treeview_lista_obiektow.insert("", END, iid=idx,
                                       values=(hotel['name'], hotel['location'],
                                               f"{hotel['lat']:.4f}, {hotel['long']:.4f}"))

        map_widget.set_marker(hotel['lat'], hotel['long'],
                              text=f"{hotel['name']}",
                              text_color="purple",
                              marker_color_circle="purple",
                              marker_color_outside="orange",
                              font=("Times New Roman", 6, "bold"))


def remove_hotel():
    selected_item_id = treeview_lista_obiektow.focus()
    if not selected_item_id:
        messagebox.showwarning("Brak zaznaczenia", "Proszę wybrać hotel do usunięcia.")
        return

    try:
        index_to_delete = int(selected_item_id)
        if 0 <= index_to_delete < len(hotels):
            hotel_name = hotels[index_to_delete]['name']
            if messagebox.askyesno("Potwierdź usunięcie", f"Czy na pewno chcesz usunąć hotel '{hotel_name}'?"):
                hotels.pop(index_to_delete)
                show_hotels()
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy indeks hotelu. Odśwież listę.")
    except ValueError:
        messagebox.showerror("Błąd", "Nie można usunąć wybranego elementu. Spróbuj ponownie.")


def edit_hotel():
    selected_item_id = treeview_lista_obiektow.focus()
    if not selected_item_id:
        messagebox.showwarning("Brak zaznaczenia", "Proszę wybrać hotel do edycji.")
        return

    try:
        index_to_edit = int(selected_item_id)
        if not (0 <= index_to_edit < len(hotels)):
            messagebox.showerror("Błąd", "Nieprawidłowy indeks hotelu. Odśwież listę.")
            return
    except ValueError:
        messagebox.showerror("Błąd", "Nie można edytować wybranego elementu. Spróbuj ponownie.")
        return

    hotel = hotels[index_to_edit]

    clear_form_entries()
    entry_name.insert(0, hotel['name'])
    entry_location.insert(0, hotel['location'])
    entry_lat.insert(0, f"{hotel['lat']:.4f}")
    entry_long.insert(0, f"{hotel['long']:.4f}")

    button_dodaj_obiekt.config(text="Zapisz zmiany", command=lambda: update_hotels(index_to_edit))


def update_hotels(i):
    new_name = entry_name.get().strip()
    new_location = entry_location.get().strip()
    new_lat_str = entry_lat.get().strip()
    new_long_str = entry_long.get().strip()

    try:
        new_lat = float(new_lat_str)
        new_long = float(new_long_str)
    except ValueError:
        messagebox.showerror("Błąd danych", "Szerokość i długość muszą być liczbami.")
        return

        return

    hotels[i]['name'] = new_name
    hotels[i]['location'] = new_location
    hotels[i]['lat'] = new_lat
    hotels[i]['long'] = new_long

    clear_form_entries()
    entry_name.focus()

    button_dodaj_obiekt.config(text="Dodaj hotel", command=add_hotel)
    show_hotels()


def show_hotel_details(event=None):
    selected_item_id = treeview_lista_obiektow.focus()
    if not selected_item_id:
        clear_details_labels()
        return

    try:
        index_to_show = int(selected_item_id)
        if not (0 <= index_to_show < len(hotels)):
            clear_details_labels()
            return
    except ValueError:
        clear_details_labels()
        return

    hotel = hotels[index_to_show]
    label_szczegoly_name_wartosc.config(text=hotel['name'])
    label_szczegoly_location_wartosc.config(text=hotel['location'])
    label_szczegoly_lat_wartosc.config(text=f"{hotel['lat']:.4f}")
    label_szczegoly_long_wartosc.config(text=f"{hotel['long']:.4f}")

    map_widget.set_position(hotel['lat'], hotel['long'])
    map_widget.set_zoom(12)
#=----------------------------------------------------------------------------------------------------=#



#=-----------------------------------------PRACOWNICY--------------------------------------------------=#
def load_default_workers():
    map_widget.delete_all_marker()  # Usuń wszystkie markery, aby narysować od nowa
    show_workers()  # Odśwież widok hoteli i mapę

def add_worker():
    worker_imie = entry_imie.get().strip()
    worker_nazwisko = entry_nazwisko.get().strip()
    hotel_name = entry_name.get().strip()         #hotel name


    worker = {'imie': worker_imie, 'nazwisko': worker_nazwisko, 'name': hotel_name}
    workers.append(worker)

    clear_form_entries()
    entry_name.focus()

    map_widget.delete_all_marker()
    show_workers()

def show_workers():
    for i in treeview_lista_obiektow.get_children():
        treeview_lista_obiektow.delete(i)

    map_widget.delete_all_marker()

    for idx, worker in enumerate(workers):
        treeview_lista_obiektow.insert("", END, iid=idx,
                                       values=(worker['imie'], worker['nazwisko'], worker['name']))

        map_widget.set_marker(hotel['lat'], hotel['long'],
                              text=f"{hotel['name']}",
                              text_color="purple",
                              marker_color_circle="purple",
                              marker_color_outside="orange",
                              font=("Times New Roman", 6, "bold"))
#...)

def remove_worker():
    selected_item_id = treeview_lista_obiektow.focus()
    if not selected_item_id:
        messagebox.showwarning("Brak zaznaczenia", "Proszę wybrać pracownika do usunięcia.")
        return

def edit_worker():
    selected_item_id = treeview_lista_obiektow.focus()
    if not selected_item_id:
        messagebox.showwarning("Brak zaznaczenia", "Proszę wybrać pracownika do edycji.")
        return

    hotel = hotels[index_to_edit]

    clear_form_entries()
    entry_imie.insert(0, worker['imie'])
    entry_nazwisko.insert(0, worker['nazwisko'])
    entry_name.insert(0, worker['name'])


    button_dodaj_obiekt.config(text="Zapisz zmiany", command=lambda: update_workers(index_to_edit))

def update_workers(i):
    worker_imie = entry_imie.get().strip()
    worker_nazwisko = entry_nazwisko.get().strip()
    worker_name = entry_name.get().strip()       #hotel name

    if not worker_name or not worker_nazwisko or not worker_imier:
        messagebox.showwarning("Brak danych", "Imię, nazwisko i nazwa hotelu nie mogą być puste.")
        return

    workers[i]['imie'] = worker_imie
    workers[i]['nazwisko'] = worker_nazwisko
    workers[i]['name'] = worker_name

    clear_form_entries()
    entry_name.focus()

    button_dodaj_obiekt.config(text="Dodaj pracownika", command=add_worker)
    show_workers()


def show_worker_details(event=None):
    selected_item_id = treeview_lista_obiektow.focus()
    if not selected_item_id:
        clear_details_labels()
        return

    try:
        index_to_show = int(selected_item_id)
        if not (0 <= index_to_show < len(workers)):
            clear_details_labels()
            return
    except ValueError:
        clear_details_labels()
        return

    worker = workers[index_to_show]
    label_szczegoly_imie_wartosc.config(text=worker['imie'])
    label_szczegoly_nazwisko_wartosc.config(text=worker['nazwisko'])
    label_szczegoly_name_wartosc.config(text=worker['name'])

    for hotel in hotels:
        if hotel['name'] == worker['name']:
            map_widget.set_position(hotel['lat'], hotel['long'])
            map_widget.set_zoom(12)
            break

def clear_form_entries():
    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_lat.delete(0, END)
    entry_long.delete(0, END)

def clear_details_labels():
    label_szczegoly_name_wartosc.config(text="....")
    label_szczegoly_location_wartosc.config(text="....")
    label_szczegoly_lat_wartosc.config(text="....")
    label_szczegoly_long_wartosc.config(text="....")
#=----------------------------------------------------------------------------------=#




def clear_form_entries():
    entry_name.delete(0, END)
    entry_location.delete(0, END)
    entry_lat.delete(0, END)
    entry_long.delete(0, END)


def clear_details_labels():
    label_szczegoly_name_wartosc.config(text="....")
    label_szczegoly_location_wartosc.config(text="....")
    label_szczegoly_lat_wartosc.config(text="....")
    label_szczegoly_long_wartosc.config(text="....")


# --- Konfiguracja głównego okna Tkinter ---
root = Tk()
root.geometry("1400x1024")
root.title("mapbook_DK")

# --- Definicja ramek głównych (relief="groove" daje obwodke) ---
# ramka_lista_obiektow i ramka_formularz zostaną zastąpione przez Notebook
ramka_szczegoly_obiektow = Frame(root, bd=2, relief="groove")
ramka_mapa = Frame(root, bd=2, relief="groove")

# --- Ułożenie ramek w gridzie ---
# Notebook zajmie miejsce ramka_lista_obiektow i ramka_formularz
notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", columnspan=3) # Notebook rozciąga się na 3 kolumny
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
ramka_mapa.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

# --- Konfiguracja wag kolumn i wierszy dla skalowania okna ---
root.grid_rowconfigure(0, weight=1)  # Notebook może rosnąć
root.grid_rowconfigure(1, weight=0)  # Ramka szczegółów ma stałą wysokość
root.grid_rowconfigure(2, weight=3)  # Mapa zajmuje większość pionowej przestrzeni
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1) # Dodana konfiguracja dla trzeciej kolumny

# --- Tworzenie zakładek ---
# Ramka dla zakładki "Hotele"
tab_hotele = ttk.Frame(notebook)
notebook.add(tab_hotele, text="Hotele")

# Ramka dla zakładki "Pracownicy"
tab_workers = ttk.Frame(notebook)
notebook.add(tab_workers, text="Pracownicy")


# Ramka dla zakładki "Goście"
tab_goscie = ttk.Frame(notebook)
notebook.add(tab_goscie, text="Goście")
Label(tab_goscie, text="Zawartość zakładki Goście (do uzupełnienia)").pack(pady=20) # Placeholder




#---------------------------TAB HOTELE-----------------------------------------------
# --- Przenosimy zawartość ramka_lista_obiektow i ramka_formularz do tab_hotele ---
# Ramki te będą teraz sub-ramkami wewnątrz tab_hotele
ramka_lista_obiektow_in_tab = Frame(tab_hotele, bd=2, relief="groove")
ramka_formularz_in_tab = Frame(tab_hotele, bd=2, relief="groove")

# Ułożenie ramek wewnątrz tab_hotele (używamy grid ponownie, ale tylko w tej ramce)
ramka_lista_obiektow_in_tab.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
ramka_formularz_in_tab.grid(row=0, column=1, padx=5, pady=5, sticky="nsew") # Formularz ma stałą szerokość

# Konfiguracja wag kolumn wewnątrz tab_hotele
tab_hotele.grid_columnconfigure(0, weight=2) # Lista hoteli może być szersza
tab_hotele.grid_columnconfigure(1, weight=1) # Formularz zajmuje mniej miejsca
tab_hotele.grid_rowconfigure(0, weight=1) # Oba elementy w 0 wierszu, rozciągają się pionowo

# --- ramka_lista_obiektow_in_tab (zawartość oryginalnej ramka_lista_obiektow) ---
label_lista_obiektow = Label(ramka_lista_obiektow_in_tab, text="Lista hoteli", font=("Arial", 12, "bold"))
label_lista_obiektow.pack(pady=5)

tree_frame = Frame(ramka_lista_obiektow_in_tab) # Zmienione rodzic na ramka_lista_obiektow_in_tab
tree_frame.pack(expand=True, fill="both")

tree_columns = ("Nazwa", "Miejscowość", "Połozenie")
treeview_lista_obiektow = ttk.Treeview(tree_frame, columns=tree_columns, show="headings")

style = ttk.Style()
style.configure("Treeview", rowheight=30, font=('Arial', 8))
style.configure("Treeview.Heading", font=('Arial', 8, 'bold'))

for col in tree_columns:
    treeview_lista_obiektow.heading(col, text=col, anchor=W)
    treeview_lista_obiektow.column(col, width=80, stretch=NO)

treeview_lista_obiektow.column("Nazwa", width=200)
treeview_lista_obiektow.column("Miejscowość", width=200, stretch=YES)
treeview_lista_obiektow.column("Połozenie", width=200)

tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=treeview_lista_obiektow.yview)
treeview_lista_obiektow.configure(yscrollcommand=tree_scrollbar.set)

tree_scrollbar.pack(side="right", fill="y")
treeview_lista_obiektow.pack(side="left", expand=True, fill="both")

list_buttons_frame = Frame(ramka_lista_obiektow_in_tab) # Zmienione rodzic na ramka_lista_obiektow_in_tab
list_buttons_frame.pack(pady=5)

button_pokaz_szczegoly_obiektu = Button(ramka_formularz_in_tab, text="Pokaż szczegóły", command=show_hotel_details, font=("Arial", 7, "bold"))
button_pokaz_szczegoly_obiektu.grid(row=7, column=1, sticky=W , pady=1) #dodane

button_remove_hotel = Button(ramka_formularz_in_tab, text="Usuń hotel", command=remove_hotel, font=("Arial", 7, "bold")) #dodane
button_remove_hotel.grid(row=8, column=1, sticky=W, pady=1) #dodane

button_edit_hotel = Button(ramka_formularz_in_tab, text="Edytuj hotel", command=edit_hotel, font=("Arial", 7, "bold")) #dodane
button_edit_hotel.grid(row=9, column=1, sticky=W, pady=1)

treeview_lista_obiektow.bind("<<TreeviewSelect>>", show_hotel_details)


# --- ramka_formularz_in_tab (zawartość oryginalnej ramka_formularz) ---
label_formularz = Label(ramka_formularz_in_tab, text="Formularz dodawania/edycji", font=("Arial", 12, "bold"))
label_formularz.grid(row=0, column=0, columnspan=2, pady=5)

pad_x_entry = 5
pad_y_entry = 3

Label(ramka_formularz_in_tab, text="Nazwa Hotelu:", anchor="w").grid(row=1, column=0, sticky=W, padx=pad_x_entry,
                                                              pady=pad_y_entry)
entry_name = Entry(ramka_formularz_in_tab, width=30)
entry_name.grid(row=1, column=1, padx=pad_x_entry, pady=pad_y_entry)

Label(ramka_formularz_in_tab, text="Miejscowość:", anchor="w").grid(row=2, column=0, sticky=W, padx=pad_x_entry,
                                                             pady=pad_y_entry)
entry_location = Entry(ramka_formularz_in_tab, width=30)
entry_location.grid(row=2, column=1, padx=pad_x_entry, pady=pad_y_entry)

Label(ramka_formularz_in_tab, text="Szerokość:", anchor="w").grid(row=3, column=0, sticky=W, padx=pad_x_entry, pady=pad_y_entry)
entry_lat = Entry(ramka_formularz_in_tab, width=30)
entry_lat.grid(row=3, column=1, padx=pad_x_entry, pady=pad_y_entry)

Label(ramka_formularz_in_tab, text="Długość:", anchor="w").grid(row=4, column=0, sticky=W, padx=pad_x_entry, pady=pad_y_entry)
entry_long = Entry(ramka_formularz_in_tab, width=30)
entry_long.grid(row=4, column=1, padx=pad_x_entry, pady=pad_y_entry)

label_lat_long_info = Label(ramka_formularz_in_tab, text="Kliknij na mapie by ustawić położenie hotelu",
                            font=("Courier New", 7, "italic"), fg="red")
label_lat_long_info.grid(row=5, column=0, columnspan=2, pady=5)

button_dodaj_obiekt = Button(ramka_formularz_in_tab, text="Dodaj hotel", command=add_hotel, font=("Arial", 10, "bold"))
button_dodaj_obiekt.grid(row=6, column=0, columnspan=2, pady=10)




#----------------------TAB WORKERS--------------------------------
# --- Przenosimy zawartość ramka_lista_obiektow i ramka_formularz do tab_pracownicy ---
# Ramki te będą teraz sub-ramkami wewnątrz tab
ramka_lista_obiektow_in_tab = Frame(tab_workers, bd=2, relief="groove")
ramka_formularz_in_tab = Frame(tab_workers, bd=2, relief="groove")

# Ułożenie ramek wewnątrz tab_workers (używamy grid ponownie, ale tylko w tej ramce)
ramka_lista_obiektow_in_tab.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
ramka_formularz_in_tab.grid(row=0, column=1, padx=5, pady=5, sticky="nsew") # Formularz ma stałą szerokość

# Konfiguracja wag kolumn wewnątrz tab_workers
tab_workers.grid_columnconfigure(0, weight=2) # Lista pracowników może być szersza
tab_workers.grid_columnconfigure(1, weight=1) # Formularz zajmuje mniej miejsca
tab_workers.grid_rowconfigure(0, weight=1) # Oba elementy w 0 wierszu, rozciągają się pionowo

# --- ramka_lista_obiektow_in_tab (zawartość oryginalnej ramka_lista_obiektow) ---
label_lista_obiektow = Label(ramka_lista_obiektow_in_tab, text="Lista pracowników", font=("Arial", 12, "bold"))
label_lista_obiektow.pack(pady=5)

tree_frame = Frame(ramka_lista_obiektow_in_tab) # Zmienione rodzic na ramka_lista_obiektow_in_tab
tree_frame.pack(expand=True, fill="both")

tree_columns = ("Imię", "Nazwisko", "Nazwa hotelu")
treeview_lista_obiektow = ttk.Treeview(tree_frame, columns=tree_columns, show="headings")

style = ttk.Style()
style.configure("Treeview", rowheight=30, font=('Arial', 8))
style.configure("Treeview.Heading", font=('Arial', 8, 'bold'))

for col in tree_columns:
    treeview_lista_obiektow.heading(col, text=col, anchor=W)
    treeview_lista_obiektow.column(col, width=80, stretch=NO)

treeview_lista_obiektow.column("Imię", width=200)
treeview_lista_obiektow.column("Nazwisko", width=200, stretch=YES)
treeview_lista_obiektow.column("Nazwa hotelu", width=200)

tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=treeview_lista_obiektow.yview)
treeview_lista_obiektow.configure(yscrollcommand=tree_scrollbar.set)

tree_scrollbar.pack(side="right", fill="y")
treeview_lista_obiektow.pack(side="left", expand=True, fill="both")

list_buttons_frame = Frame(ramka_lista_obiektow_in_tab) # Zmienione rodzic na ramka_lista_obiektow_in_tab
list_buttons_frame.pack(pady=5)

button_pokaz_szczegoly_obiektu = Button(ramka_formularz_in_tab, text="Pokaż szczegóły", command=show_worker_details, font=("Arial", 7, "bold"))
button_pokaz_szczegoly_obiektu.grid(row=7, column=1, sticky=W , pady=1) #dodane

button_remove_worker = Button(ramka_formularz_in_tab, text="Usuń pracownika", command=remove_hotel, font=("Arial", 7, "bold")) #dodane
button_remove_worker.grid(row=8, column=1, sticky=W, pady=1) #dodane

button_edit_worker = Button(ramka_formularz_in_tab, text="Edytuj pracownika", command=edit_hotel, font=("Arial", 7, "bold")) #dodane
button_edit_worker.grid(row=9, column=1, sticky=W, pady=1)

treeview_lista_obiektow.bind("<<TreeviewSelect>>", show_hotel_details)


# --- ramka_formularz_in_tab (zawartość oryginalnej ramka_formularz) ---
label_formularz = Label(ramka_formularz_in_tab, text="Formularz dodawania/edycji", font=("Arial", 12, "bold"))
label_formularz.grid(row=0, column=0, columnspan=2, pady=5)

pad_x_entry = 5
pad_y_entry = 3

Label(ramka_formularz_in_tab, text="Imię:", anchor="w").grid(row=1, column=0, sticky=W, padx=pad_x_entry,
                                                              pady=pad_y_entry)
entry_imie = Entry(ramka_formularz_in_tab, width=30)
entry_imie.grid(row=1, column=1, padx=pad_x_entry, pady=pad_y_entry)

Label(ramka_formularz_in_tab, text="Nazwisko:", anchor="w").grid(row=2, column=0, sticky=W, padx=pad_x_entry,
                                                             pady=pad_y_entry)
entry_surename = Entry(ramka_formularz_in_tab, width=30)
entry_surename.grid(row=2, column=1, padx=pad_x_entry, pady=pad_y_entry)

Label(ramka_formularz_in_tab, text="Hotel:", anchor="w").grid(row=3, column=0, sticky=W, padx=pad_x_entry,
                                                              pady=pad_y_entry)

entry_surename = Entry(ramka_formularz_in_tab, width=30)
entry_surename.grid(row=2, column=1, padx=pad_x_entry, pady=pad_y_entry)

entry_name = Entry(ramka_formularz_in_tab, width=30)
entry_name.grid(row=3, column=1, padx=pad_x_entry, pady=pad_y_entry)

label_lat_long_info.grid(row=5, column=0, columnspan=2, pady=5)

button_dodaj_obiekt = Button(ramka_formularz_in_tab, text="Dodaj pracownika", command=add_hotel, font=("Arial", 10, "bold"))
button_dodaj_obiekt.grid(row=6, column=0, columnspan=2, pady=10)








#--------------------------------------------------------------------------
# --- ramka_szczegoly_obiektow (bez zmian, nie jest w tabie) ---
label_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Szczegóły hotelu:", font=("Arial", 12, "bold"))
label_szczegoly_obiektu.grid(row=0, column=0, columnspan=8, pady=5)

pad_x_details = 5
pad_y_details = 2

Label(ramka_szczegoly_obiektow, text="Nazwa:", anchor="w", font=("Arial", 9, "bold")).grid(row=1, column=0, sticky=W,
                                                                                           padx=pad_x_details,
                                                                                           pady=pad_y_details)
label_szczegoly_name_wartosc = Label(ramka_szczegoly_obiektow, text="....", anchor="w")
label_szczegoly_name_wartosc.grid(row=1, column=1, sticky=W, padx=pad_x_details, pady=pad_y_details)

Label(ramka_szczegoly_obiektow, text="Miejscowość:", anchor="w", font=("Arial", 9, "bold")).grid(row=1, column=2,
                                                                                                 sticky=W,
                                                                                                 padx=pad_x_details,
                                                                                                 pady=pad_y_details)
label_szczegoly_location_wartosc = Label(ramka_szczegoly_obiektow, text="....", anchor="w")
label_szczegoly_location_wartosc.grid(row=1, column=3, sticky=W, padx=pad_x_details, pady=pad_y_details)

Label(ramka_szczegoly_obiektow, text="Szerokość:", anchor="w", font=("Arial", 9, "bold")).grid(row=1, column=4,
                                                                                               sticky=W,
                                                                                               padx=pad_x_details,
                                                                                               pady=pad_y_details)
label_szczegoly_lat_wartosc = Label(ramka_szczegoly_obiektow, text="....", anchor="w")
label_szczegoly_lat_wartosc.grid(row=1, column=5, sticky=W, padx=pad_x_details, pady=pad_y_details)

Label(ramka_szczegoly_obiektow, text="Długość:", anchor="w", font=("Arial", 9, "bold")).grid(row=1, column=6, sticky=W,
                                                                                             padx=pad_x_details,
                                                                                             pady=pad_y_details)
label_szczegoly_long_wartosc = Label(ramka_szczegoly_obiektow, text="....", anchor="w")
label_szczegoly_long_wartosc.grid(row=1, column=7, sticky=W, padx=pad_x_details, pady=pad_y_details)

for i in range(8):
    ramka_szczegoly_obiektow.grid_columnconfigure(i, weight=1)

# --- ramka_mapa (bez zmian, nie jest w tabie) ---
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=1200, height=500, corner_radius=5)
map_widget.pack(fill="both", expand=True)
map_widget.set_position(52.23, 21.0)
map_widget.set_zoom(6)


def add_marker_on_click(coordinates_tuple):
    map_widget.delete_all_marker()
    latitude, longitude = coordinates_tuple[0], coordinates_tuple[1]

    entry_lat.delete(0, END)
    entry_lat.insert(0, f"{latitude:.4f}")
    entry_long.delete(0, END)
    entry_long.insert(0, f"{longitude:.4f}")

    map_widget.set_marker(latitude, longitude, font=("Times New Roman", 8, "bold"), text_color="red", text="Wybrano")


map_widget.add_left_click_map_command(add_marker_on_click)

root.after(1000, load_default_hotels)

root.mainloop()
#>>>>>>> 
main

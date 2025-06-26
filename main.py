from tkinter import * #Importuje wszystkie klasy i funkcje z biblioteki tkinter, służącej do tworzenia graficznych interfejsów użytkownika (GUI)
from tkinter import ttk #Importuje ttk – nowoczesne widżety (np. Treeview, Combobox)
import tkintermapview #Importuje zewnętrzny moduł tkintermapview, który pozwala wyświetlać mapy OpenStreetMap w aplikacji tkinter
from tkinter import messagebox #Importuje moduł messagebox do wyświetlania okienek z komunikatami (błędy, potwierdzenia, ostrzeżenia itd.)

# --- Globalne listy danych i stałe ---
hotels: list = [] #pusta lista hoteli
employees: list = [] #tworzy pustą listę pracowników
guests: list = [] #tworzy pustą listę gości
current_tab = "hotels" #Określa, która zakładka (widok) w GUI jest aktywna — domyślnie "hotels"
#Stała z tekstem pomocniczym do pola filtrowania hoteli.
FILTER_PLACEHOLDER_TEXT = "Filtruj po nazwie hotelu..."



def load_default_test_data():
    # Domyślne hotele
    hotels.append({'name': 'Hotel1', 'location': 'Warszawa', 'lat': 52.237049, 'long': 21.017532}) #Dodaje słowniki reprezentujące hotele z nazwą, lokalizacją i współrzędnymi (lat, long) do listy hotels
    hotels.append({'name': 'Hotel2', 'location': 'Gdansk', 'lat': 54.372158, 'long': 18.638306})
    hotels.append({'name': 'Hotel3', 'location': 'Krakow', 'lat': 50.0647, 'long': 19.9450})
    hotels.append({'name': 'Sobieski', 'location': 'Poznan', 'lat': 52.40, 'long': 16.91})
    hotels.append({'name': 'Novotel1', 'location': 'Wroclaw', 'lat': 51.14, 'long': 17.0})
    hotels.append({'name': 'Novotel2', 'location': 'Lublin', 'lat': 51.1954, 'long': 22.7578})

    # Domyślni pracownicy
    employees.append({'imie_nazwisko': 'Jan Kowalski', 'miejsce_zamieszkania': 'Warszawa', 'lat': 52.2370, 'long': 21.017, 'hotel_name': 'Hotel1'})
    employees.append({'imie_nazwisko': 'Anna Nowak', 'miejsce_zamieszkania': 'Gdansk', 'lat': 54.372, 'long': 18.638, 'hotel_name': 'Hotel2'})
    employees.append({'imie_nazwisko': 'Piotr Zakoscielny', 'miejsce_zamieszkania': 'Krakow', 'lat': 53.372, 'long': 19.638, 'hotel_name': 'Hotel2'})
    employees.append({'imie_nazwisko': 'Grzegorz Moscicki', 'miejsce_zamieszkania': 'Krakow', 'lat': 52.372, 'long': 17.638, 'hotel_name': 'Hotel2'})
    employees.append({'imie_nazwisko': 'Slawek Sikorski', 'miejsce_zamieszkania': 'Poznan', 'lat': 51.372, 'long': 18.638, 'hotel_name': 'Sobieski'})
    employees.append({'imie_nazwisko': 'Maciej Prosty', 'miejsce_zamieszkania': 'Poznan', 'lat': 52.372, 'long': 16.91, 'hotel_name': 'Sobieski'})

    # Domyślni goście
    guests.append({'imie_nazwisko': 'Tomek Podroznik', 'adres_zamieszkania': 'Poznań', 'lat': 52.4064, 'long': 16.9252, 'hotel_name': 'Hotel2'})
    guests.append({'imie_nazwisko': 'Ewa Wypoczynska', 'adres_zamieszkania': 'Wrocław', 'lat': 51.1079, 'long': 17.0385,'hotel_name': 'Hotel3'})
    guests.append({'imie_nazwisko': 'Wanda Moczydlo', 'adres_zamieszkania': 'Warszawa', 'lat': 52.2370, 'long': 21.017,'hotel_name': 'Sobieski'})
    guests.append({'imie_nazwisko': 'Stefan Batory', 'adres_zamieszkania': 'Krakow', 'lat':  52.372, 'long': 17.638,'hotel_name': 'Sobieski'})
    guests.append({'imie_nazwisko': 'Janko Baca', 'adres_zamieszkania': 'Zakopane', 'lat':  49.5943, 'long': 21.2635,'hotel_name': 'Hotel1'})

    #
    map_widget.delete_all_marker() # czyczenie markerow na mapie
    show_hotels() # pokaz wszystkie hotele
    update_hotel_dropdown() # dodaje wszystkie hotele to listy dropdown uzytej w formularzu gosci/pracownikow


def showOnMap(lat, long, name):
    #Dodaje pinezkę (marker) na mapie w podanej lokalizacji z etykietą i kolorem.
    map_widget.set_marker(lat, long, text=f"{name}", text_color="purple", marker_color_circle="purple",
                          marker_color_outside="orange", font=("Times New Roman", 6, "bold"))


def update_hotel_dropdown():
    hotel_names = [h['name'] for h in hotels] #Tworzy listę nazw hoteli.
    hotel_combobox['values'] = hotel_names #Ustawia wartości w polu Combobox
    current_selection = hotel_combobox.get() #Jeśli bieżący wybór nie istnieje w nowych danych, czyści pole wyboru.
    if current_selection not in hotel_names:
        hotel_combobox.set('')


## Hotele ##############################################################################

def add_hotel():
    hotel_nazwa = entry_name.get().strip()
    hotel_miejscowosc = entry_location.get().strip()
    hotel_lat_str = entry_lat.get().strip()
    hotel_long_str = entry_long.get().strip()
    #Pobiera dane z pól formularza (entry_name, entry_location, entry_lat, entry_long).
    try:
        hotel_lat = float(hotel_lat_str)
        hotel_long = float(hotel_long_str)
        #Konwertuje współrzędne na float. Jeśli nie można – pokazuje błąd.
    except ValueError:
        messagebox.showerror("Błąd danych", "Kliknij na mapie by wybrac Polozenie hotelu")
        #Sprawdza, czy nazwa i miejscowość są niepuste.
        return
    if not hotel_nazwa or not hotel_miejscowosc:
        messagebox.showwarning("Brak danych", "Nazwa hotelu i miejscowość nie mogą być puste.")
        return

    # Walidacja unikalności nazwy niewrażliwa na wielkość liter
    if any(h['name'].lower() == hotel_nazwa.lower() for h in hotels):
        messagebox.showerror("Błąd",
                             f"Hotel o nazwie '{hotel_nazwa}' już istnieje. Nazwa musi być unikalna (wielkość liter nie ma znaczenia).")
       #Sprawdza, czy hotel o tej samej nazwie już istnieje (ignorując wielkość liter).
        return

    hotel = {'name': hotel_nazwa, 'location': hotel_miejscowosc, 'lat': hotel_lat, 'long': hotel_long}
    hotels.append(hotel)
    clear_form_entries()
    entry_name.focus()
    show_hotels()
    update_hotel_dropdown()
    #Jeśli dane są poprawne, tworzy słownik hotelu, dodaje go do listy, czyści formularz i odświeża widok.


def remove_hotel():
    selected_item_id = treeview_lista_obiektow.focus() #Pobiera ID zaznaczonego elementu z listy (treeview_lista_obiektow).
    if not selected_item_id: return #Jeśli użytkownik potwierdzi usunięcie, usuwa hotel z listy hotels.
    try:
        index_to_delete = int(selected_item_id)
        if 0 <= index_to_delete < len(hotels):
            hotel_name_to_delete = hotels[index_to_delete]['name']
            if messagebox.askyesno("Potwierdź usunięcie",
                                   f"Czy na pewno chcesz usunąć hotel '{hotel_name_to_delete}'?"):
                employees_in_hotel = [emp for emp in employees if emp.get('hotel_name') == hotel_name_to_delete]
                guests_in_hotel = [g for g in guests if g.get('hotel_name') == hotel_name_to_delete]
                if (employees_in_hotel or guests_in_hotel) and not messagebox.askyesno("Ostrzeżenie",
                                                                                       "Do tego hotelu przypisani są pracownicy lub goście. Czy na pewno chcesz kontynuować? (Stracą oni przypisanie)."):
                    #Jeśli hotel miał przypisanych gości/pracowników, ostrzega i resetuje ich przypisanie.
                    return

                for emp in employees:
                    if emp.get('hotel_name') == hotel_name_to_delete: emp['hotel_name'] = "Brak (usunięty)"
                for g in guests:
                    if g.get('hotel_name') == hotel_name_to_delete: g['hotel_name'] = "Brak (usunięty)"

                hotels.pop(index_to_delete)
                show_hotels()
                update_hotel_dropdown()
                #Odświeża widok i dropdown.
    except ValueError:
        pass


def edit_hotel():
    selected_item_id = treeview_lista_obiektow.focus() #Pobiera ID zaznaczonego wiersza (hotelu) z Treeview – komponentu listy GUI.
    #focus() zwraca identyfikator wybranego elementu.
    if not selected_item_id: return #Jeśli nic nie zaznaczono – kończy działanie funkcji.
    try:
        index_to_edit = int(selected_item_id) #Przekształca ID z Treeview na liczbę całkowitą (indeks listy hotels).
        if not (0 <= index_to_edit < len(hotels)): return #Sprawdza, czy indeks mieści się w zakresie listy.
        hotel = hotels[index_to_edit] #Pobiera dane hotelu o wskazanym indeksie.
        clear_form_entries() #Czyści pola formularza (nazwa, lokalizacja, współrzędne) przed wpisaniem nowych danych.
        #Wstawia aktualne dane hotelu do odpowiednich pól tekstowych (Entry).
        #Współrzędne są zaokrąglane do 4 miejsc po przecinku.
        entry_name.insert(0, hotel['name']);
        entry_location.insert(0, hotel['location'])
        entry_lat.insert(0, f"{hotel['lat']:.4f}");
        entry_long.insert(0, f"{hotel['long']:.4f}")
        #Zmienia tekst przycisku z „Dodaj hotel” na „Zapisz zmiany”.
        #Podpina nową funkcję update_hotels, która zapisze edytowane dane po kliknięciu.
        button_dodaj_obiekt.config(text="Zapisz zmiany", command=lambda: update_hotels(index_to_edit))
    except ValueError:
        pass
    #W razie błędnej konwersji na int – ignoruje błąd (np. ID nie było liczbą).


def update_hotels(i):
    old_name = hotels[i]['name'] #Zapisuje starą nazwę hotelu (przyda się np. do aktualizacji przypisanych gości/pracowników.
    new_name, new_location = entry_name.get().strip(), entry_location.get().strip() #Pobiera wpisane dane z formularza i usuwa białe znaki z początku/końca.
    new_lat_str, new_long_str = entry_lat.get().strip(), entry_long.get().strip() #Pobiera wpisane współrzędne jako ciągi znaków.
    if not new_name or not new_location: messagebox.showwarning("Brak danych", "Pola nie mogą być puste."); return #Jeśli nazwa lub miejscowość są puste – pokazuje ostrzeżenie i przerywa.
    try:
        new_lat, new_long = float(new_lat_str), float(new_long_str)
    except ValueError:
        messagebox.showerror("Błąd danych", "Szerokość i długość muszą być liczbami."); return

    # Walidacja unikalności nazwy niewrażliwa na wielkość liter przy edycji
    for index, h in enumerate(hotels):
        if h['name'].lower() == new_name.lower() and i != index:
            messagebox.showerror("Błąd",
                                 f"Hotel o nazwie '{new_name}' już istnieje. Nazwa musi być unikalna (wielkość liter nie ma znaczenia).")
            return

    hotels[i].update({'name': new_name, 'location': new_location, 'lat': new_lat, 'long': new_long})
    if old_name != new_name:
        for emp in employees:
            if emp.get('hotel_name') == old_name: emp['hotel_name'] = new_name
        for g in guests:
            if g.get('hotel_name') == old_name: g['hotel_name'] = new_name

    clear_form_entries()
    entry_name.focus()
    button_dodaj_obiekt.config(text="Dodaj hotel", command=add_hotel)
    show_hotels()
    update_hotel_dropdown()


def show_hotels(filter_text=""):
    for i in treeview_lista_obiektow.get_children(): treeview_lista_obiektow.delete(i)
    map_widget.delete_all_marker()

    display_list = [hotel for hotel in hotels if
                    filter_text.lower() in hotel.get('name', '').lower()] if filter_text else hotels

    for hotel in display_list:
        original_idx = hotels.index(hotel)
        treeview_lista_obiektow.insert("", END, iid=original_idx, values=(hotel['name'], hotel['location'],
                                                                 f"{hotel['lat']:.4f}, {hotel['long']:.4f}"))
        showOnMap(hotel['lat'], hotel['long'], hotel['name'])
    map_widget.set_zoom(5)

## Pracownicy ##########################################################################

def show_employees(filter_text=""):
    for i in treeview_lista_obiektow.get_children(): treeview_lista_obiektow.delete(i)
    map_widget.delete_all_marker()

    display_list = [emp for emp in employees if
                    filter_text.lower() in emp.get('hotel_name', '').lower()] if filter_text else employees

    for employee in display_list:
        original_idx = employees.index(employee)
        hotel_name = employee.get('hotel_name', 'Brak')
        treeview_lista_obiektow.insert("", END, iid=original_idx,
                                       values=(hotel_name, employee['imie_nazwisko'], employee['miejsce_zamieszkania'],
                                               f"{employee['lat']:.4f}, {employee['long']:.4f}"),
                                       tags=('employee_item',))
        showOnMap(employee['lat'], employee['long'], employee['imie_nazwisko'])
    map_widget.set_zoom(5)

def add_employee():
    assigned_hotel = hotel_combobox.get()
    if not assigned_hotel: messagebox.showwarning("Brak hotelu", "Proszę wybrać hotel z listy."); return
    imie_nazwisko, miejsce_zamieszkania = entry_name.get().strip(), entry_location.get().strip()
    lat_str, long_str = entry_lat.get().strip(), entry_long.get().strip()
    try:
        lat, long = float(lat_str), float(long_str)
    except ValueError:
        messagebox.showerror("Błąd danych", "Kliknij na mapie by wybrać Położenie pracownika."); return
    if not imie_nazwisko or not miejsce_zamieszkania: messagebox.showwarning("Brak danych",
                                                                             "Pola nie mogą być puste."); return
    employees.append(
        {'imie_nazwisko': imie_nazwisko, 'miejsce_zamieszkania': miejsce_zamieszkania, 'lat': lat, 'long': long,
         'hotel_name': assigned_hotel})
    clear_form_entries();
    entry_name.focus();
    show_employees()


def remove_employee():
    selected_item_id = treeview_lista_obiektow.focus()
    if not selected_item_id: return
    try:
        index_to_delete = int(selected_item_id)
        if 0 <= index_to_delete < len(employees) and messagebox.askyesno("Potwierdź usunięcie",
                                                                         f"Czy na pewno chcesz usunąć pracownika '{employees[index_to_delete]['imie_nazwisko']}'?"):
            employees.pop(index_to_delete)
            on_filter_change()  # Odśwież widok z filtrem
    except ValueError:
        pass


def edit_employee():
    selected_item_id = treeview_lista_obiektow.focus()
    if not selected_item_id: return
    try:
        index_to_edit = int(selected_item_id)
        if not (0 <= index_to_edit < len(employees)): return
        employee = employees[index_to_edit]
        clear_form_entries()
        entry_name.insert(0, employee['imie_nazwisko']);
        entry_location.insert(0, employee['miejsce_zamieszkania'])
        entry_lat.insert(0, f"{employee['lat']:.4f}");
        entry_long.insert(0, f"{employee['long']:.4f}")
        hotel_combobox.set(employee.get('hotel_name', ''))
        button_dodaj_obiekt.config(text="Zapisz zmiany", command=lambda: update_employee(index_to_edit))
    except ValueError:
        pass


def update_employee(i):
    assigned_hotel = hotel_combobox.get()
    if not assigned_hotel: return
    new_imie_nazwisko, new_miejsce_zamieszkania = entry_name.get().strip(), entry_location.get().strip()
    new_lat_str, new_long_str = entry_lat.get().strip(), entry_long.get().strip()
    try:
        new_lat, new_long = float(new_lat_str), float(new_long_str)
    except ValueError:
        messagebox.showerror("Błąd danych", "Szerokość i długość muszą być liczbami."); return
    if not new_imie_nazwisko or not new_miejsce_zamieszkania: return
    employees[i].update(
        {'imie_nazwisko': new_imie_nazwisko, 'miejsce_zamieszkania': new_miejsce_zamieszkania, 'lat': new_lat,
         'long': new_long, 'hotel_name': assigned_hotel})
    clear_form_entries();
    entry_name.focus()
    button_dodaj_obiekt.config(text="Dodaj pracownika", command=add_employee)
    on_filter_change()


## Goście ##################################################################################

def show_guests(filter_text=""):
    for i in treeview_lista_obiektow.get_children(): treeview_lista_obiektow.delete(i)
    map_widget.delete_all_marker()

    display_list = [g for g in guests if
                    filter_text.lower() in g.get('hotel_name', '').lower()] if filter_text else guests

    for guest in display_list:
        original_idx = guests.index(guest)
        hotel_name = guest.get('hotel_name', 'Brak')
        treeview_lista_obiektow.insert("", END, iid=original_idx,
                                       values=(hotel_name, guest['imie_nazwisko'], guest['adres_zamieszkania'],
                                               f"{guest['lat']:.4f}, {guest['long']:.4f}"), tags=('guest_item',))
        showOnMap(guest['lat'], guest['long'], guest['imie_nazwisko'])
    map_widget.set_zoom(5)

def add_guest():
    assigned_hotel = hotel_combobox.get()
    if not assigned_hotel: messagebox.showwarning("Brak hotelu", "Proszę wybrać hotel z listy."); return
    imie_nazwisko, adres_zamieszkania = entry_name.get().strip(), entry_location.get().strip()
    lat_str, long_str = entry_lat.get().strip(), entry_long.get().strip()
    try:
        lat, long = float(lat_str), float(long_str)
    except ValueError:
        messagebox.showerror("Błąd danych", "Kliknij na mapie by wybrać lokalizację gościa."); return
    if not imie_nazwisko or not adres_zamieszkania: messagebox.showwarning("Brak danych",
                                                                           "Pola nie mogą być puste."); return
    guests.append({'imie_nazwisko': imie_nazwisko, 'adres_zamieszkania': adres_zamieszkania, 'lat': lat, 'long': long,
                   'hotel_name': assigned_hotel})
    clear_form_entries();
    entry_name.focus();
    show_guests()


def remove_guest():
    selected_item_id = treeview_lista_obiektow.focus()
    if not selected_item_id: return
    try:
        index_to_delete = int(selected_item_id)
        if 0 <= index_to_delete < len(guests) and messagebox.askyesno("Potwierdź usunięcie",
                                                                      f"Czy na pewno chcesz usunąć gościa '{guests[index_to_delete]['imie_nazwisko']}'?"):
            guests.pop(index_to_delete)
            on_filter_change()
    except ValueError:
        pass


def edit_guest():
    selected_item_id = treeview_lista_obiektow.focus()
    if not selected_item_id: return
    try:
        index_to_edit = int(selected_item_id)
        if not (0 <= index_to_edit < len(guests)): return
        guest = guests[index_to_edit]
        clear_form_entries()
        entry_name.insert(0, guest['imie_nazwisko']);
        entry_location.insert(0, guest['adres_zamieszkania'])
        entry_lat.insert(0, f"{guest['lat']:.4f}");
        entry_long.insert(0, f"{guest['long']:.4f}")
        hotel_combobox.set(guest.get('hotel_name', ''))
        button_dodaj_obiekt.config(text="Zapisz zmiany", command=lambda: update_guest(index_to_edit))
    except ValueError:
        pass


def update_guest(i):
    assigned_hotel = hotel_combobox.get()
    if not assigned_hotel: return
    new_imie_nazwisko, new_adres_zamieszkania = entry_name.get().strip(), entry_location.get().strip()
    new_lat_str, new_long_str = entry_lat.get().strip(), entry_long.get().strip()
    try:
        new_lat, new_long = float(new_lat_str), float(new_long_str)
    except ValueError:
        messagebox.showerror("Błąd danych", "Szerokość i długość muszą być liczbami."); return
    if not new_imie_nazwisko or not new_adres_zamieszkania: return
    guests[i].update({'imie_nazwisko': new_imie_nazwisko, 'adres_zamieszkania': new_adres_zamieszkania, 'lat': new_lat,
                      'long': new_long, 'hotel_name': assigned_hotel})
    clear_form_entries();
    entry_name.focus()
    button_dodaj_obiekt.config(text="Dodaj gościa", command=add_guest)
    on_filter_change()


## Funkcje pomocnicze i UI ################################################################

def on_filter_change(event=None):
    filter_text = filter_entry.get().strip()
    if filter_text == FILTER_PLACEHOLDER_TEXT:
        filter_text = ""
    if current_tab == "employees":
        show_employees(filter_text)
    elif current_tab == "guests":
        show_guests(filter_text)
    elif current_tab == "hotels":
        show_hotels(filter_text)


def setup_filter_placeholder():
    filter_entry.insert(0, FILTER_PLACEHOLDER_TEXT);
    filter_entry.config(fg='grey')

    def on_focus_in(event):
        if filter_entry.get() == FILTER_PLACEHOLDER_TEXT:
            filter_entry.delete(0, END);
            filter_entry.config(fg='black')

    def on_focus_out(event):
        if not filter_entry.get():
            filter_entry.insert(0, FILTER_PLACEHOLDER_TEXT);
            filter_entry.config(fg='grey')

    filter_entry.bind("<FocusIn>", on_focus_in);
    filter_entry.bind("<FocusOut>", on_focus_out)


def handle_escape_key(event=None):
    clear_form_entries()
    treeview_lista_obiektow.selection_remove(treeview_lista_obiektow.selection())
    clear_details_labels()
    filter_entry.delete(0, END);
    setup_filter_placeholder();
    on_filter_change()

    if current_tab == "hotels":
        button_dodaj_obiekt.config(text="Dodaj hotel", command=add_hotel)
        show_hotels()
    elif current_tab == "employees":
        button_dodaj_obiekt.config(text="Dodaj pracownika", command=add_employee)
        show_employees()
    elif current_tab == "guests":
        button_dodaj_obiekt.config(text="Dodaj gościa", command=add_guest)
        show_guests()


def show_item_details(event=None):
    selected_item_id = treeview_lista_obiektow.focus()
    clear_details_labels()
    if not selected_item_id: return
    try:
        index_to_show = int(selected_item_id)
    except ValueError:
        return

    obj = None
    if current_tab == "hotels" and 0 <= index_to_show < len(hotels):
        obj = hotels[index_to_show]
        label_szczegoly_name_wartosc.config(text=obj['name']);
        label_szczegoly_location_wartosc.config(text=obj['location']);
        label_szczegoly_hotel_wartosc.config(text="---")
    elif current_tab == "employees" and 0 <= index_to_show < len(employees):
        obj = employees[index_to_show]
        label_szczegoly_name_wartosc.config(text=obj['imie_nazwisko']);
        label_szczegoly_location_wartosc.config(text=obj['miejsce_zamieszkania']);
        label_szczegoly_hotel_wartosc.config(text=obj.get('hotel_name', 'Brak'))
    elif current_tab == "guests" and 0 <= index_to_show < len(guests):
        obj = guests[index_to_show]
        label_szczegoly_name_wartosc.config(text=obj['imie_nazwisko']);
        label_szczegoly_location_wartosc.config(text=obj['adres_zamieszkania']);
        label_szczegoly_hotel_wartosc.config(text=obj.get('hotel_name', 'Brak'))
    else:
        return

    label_szczegoly_lat_wartosc.config(text=f"{obj['lat']:.4f}");
    label_szczegoly_long_wartosc.config(text=f"{obj['long']:.4f}")
    map_widget.delete_all_marker();
    showOnMap(obj['lat'], obj['long'], obj.get('name') or obj.get('imie_nazwisko'))
    map_widget.set_position(obj['lat'], obj['long']);
    map_widget.set_zoom(8)


def clear_form_entries():
    entry_name.delete(0, END);
    entry_location.delete(0, END)
    entry_lat.delete(0, END);
    entry_long.delete(0, END);
    hotel_combobox.set('')


def clear_details_labels():
    for label in [label_szczegoly_name_wartosc, label_szczegoly_location_wartosc, label_szczegoly_lat_wartosc,
                  label_szczegoly_long_wartosc, label_szczegoly_hotel_wartosc]:
        label.config(text="....")


def notebook_tab_changed(event):
    global current_tab
    selected_tab_text = notebook.tab(notebook.select(), "text")
    clear_form_entries();
    clear_details_labels()
    treeview_lista_obiektow.selection_remove(treeview_lista_obiektow.selection())
    for i in treeview_lista_obiektow.get_children(): treeview_lista_obiektow.delete(i)
    map_widget.delete_all_marker()
    filter_entry.delete(0, END);
    setup_filter_placeholder()

    if selected_tab_text == "Hotele":
        current_tab = "hotels"
        # filter_entry.pack_forget()
        filter_entry.pack(side="left", padx=10, fill=X, expand=True)
        label_hotel_select.grid_remove();
        hotel_combobox.grid_remove()
        treeview_lista_obiektow.config(columns=("Nazwa", "Miejscowość", "Położenie"))
        treeview_lista_obiektow.heading("Nazwa", text="Nazwa Hotelu");
        treeview_lista_obiektow.column("Nazwa", width=200)
        treeview_lista_obiektow.heading("Miejscowość", text="Miejscowość");
        treeview_lista_obiektow.column("Miejscowość", width=200)
        treeview_lista_obiektow.heading("Położenie", text="Położenie");
        treeview_lista_obiektow.column("Położenie", width=200)
        label_formularz.config(text="Formularz dodawania/edycji hotelu");
        label_name.config(text="Nazwa Hotelu:");
        label_location.config(text="Miejscowość:")
        button_dodaj_obiekt.config(text="Dodaj hotel", command=add_hotel);
        button_usun_obiekt.config(command=remove_hotel, text="Usuń hotel");
        button_edytuj_obiekt.config(command=edit_hotel, text="Edytuj hotel")
        label_lista_obiektow.config(text="Lista hoteli");
        label_szczegoly_name.config(text="Nazwa Hotelu")
        show_hotels()
    else:
        filter_entry.pack(side="left", padx=10, fill=X, expand=True)
        label_hotel_select.grid();
        hotel_combobox.grid();
        update_hotel_dropdown()
        if selected_tab_text == "Pracownicy":
            current_tab = "employees"
            cols = ("Nazwa Hotelu", "Imię i Nazwisko", "Miejsce Zamieszkania", "Położenie")
            treeview_lista_obiektow.config(columns=cols)
            treeview_lista_obiektow.heading(cols[0], text=cols[0]);
            treeview_lista_obiektow.column(cols[0], width=150)
            treeview_lista_obiektow.heading(cols[1], text=cols[1]);
            treeview_lista_obiektow.column(cols[1], width=200)
            treeview_lista_obiektow.heading(cols[2], text=cols[2]);
            treeview_lista_obiektow.column(cols[2], width=200)
            treeview_lista_obiektow.heading(cols[3], text=cols[3]);
            treeview_lista_obiektow.column(cols[3], width=150)
            label_formularz.config(text="Formularz dodawania/edycji pracownika");
            label_name.config(text="Imię i Nazwisko:");
            label_location.config(text="Miejsce Zamieszkania:")
            button_dodaj_obiekt.config(text="Dodaj pracownika", command=add_employee);
            button_usun_obiekt.config(command=remove_employee, text="Usuń pracownika");
            button_edytuj_obiekt.config(command=edit_employee, text="Edytuj pracownika")
            label_lista_obiektow.config(text="Lista pracowników");
            label_szczegoly_name.config(text="Imię i Nazwisko")
            show_employees()
        else:  # Goście
            current_tab = "guests"
            cols = ("Nazwa Hotelu", "Imię i Nazwisko", "Adres Zamieszkania", "Położenie")
            treeview_lista_obiektow.config(columns=cols)
            treeview_lista_obiektow.heading(cols[0], text=cols[0]);
            treeview_lista_obiektow.column(cols[0], width=150)
            treeview_lista_obiektow.heading(cols[1], text=cols[1]);
            treeview_lista_obiektow.column(cols[1], width=200)
            treeview_lista_obiektow.heading(cols[2], text=cols[2]);
            treeview_lista_obiektow.column(cols[2], width=200)
            treeview_lista_obiektow.heading(cols[3], text=cols[3]);
            treeview_lista_obiektow.column(cols[3], width=150)
            label_formularz.config(text="Formularz dodawania/edycji gościa");
            label_name.config(text="Imię i Nazwisko:");
            label_location.config(text="Adres Zamieszkania:")
            button_dodaj_obiekt.config(text="Dodaj gościa", command=add_guest);
            button_usun_obiekt.config(command=remove_guest, text="Usuń gościa");
            button_edytuj_obiekt.config(command=edit_guest, text="Edytuj gościa")
            label_lista_obiektow.config(text="Lista gości");
            label_szczegoly_name.config(text="Imię i Nazwisko")
            show_guests()


# --- Konfiguracja głównego okna Tkinter ---
root = Tk();
root.geometry("1200x800");
root.title("System Zarządzania Hotelami");
root.minsize(1000, 700)
ramka_szczegoly_obiektow = Frame(root, bd=2, relief="groove");
ramka_mapa = Frame(root, bd=2, relief="groove")
notebook = ttk.Notebook(root);
tab_hotele = ttk.Frame(notebook);
notebook.add(tab_hotele, text="Hotele");
tab_pracownicy = ttk.Frame(notebook);
notebook.add(tab_pracownicy, text="Pracownicy");
tab_goscie = ttk.Frame(notebook);
notebook.add(tab_goscie, text="Goście");
notebook.bind("<<NotebookTabChanged>>", notebook_tab_changed)
ramka_lista_obiektow = Frame(root, bd=2, relief="groove");
ramka_formularz = Frame(root, bd=2, relief="groove")
notebook.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew");
ramka_lista_obiektow.grid(row=1, column=0, padx=5, pady=5, sticky="nsew");
ramka_formularz.grid(row=1, column=1, padx=5, pady=5, sticky="nsew");
ramka_szczegoly_obiektow.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew");
ramka_mapa.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
root.grid_rowconfigure(1, weight=2);
root.grid_rowconfigure(3, weight=3);
root.grid_columnconfigure(0, weight=3);
root.grid_columnconfigure(1, weight=2)

# --- ramka_lista_obiektow ---
label_lista_obiektow = Label(ramka_lista_obiektow, text="Lista", font=("Arial", 12, "bold"));
label_lista_obiektow.pack(pady=5)
tree_frame = Frame(ramka_lista_obiektow);
tree_frame.pack(expand=True, fill="both")
treeview_lista_obiektow = ttk.Treeview(tree_frame, show="headings", height=7)
style = ttk.Style();
style.configure("Treeview", rowheight=30, font=('Arial', 9));
style.configure("Treeview.Heading", font=('Arial', 9, 'bold'));
style.configure('employee_item', foreground='green');
style.configure('guest_item', foreground='darkred')
tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=treeview_lista_obiektow.yview);
treeview_lista_obiektow.configure(yscrollcommand=tree_scrollbar.set)
tree_scrollbar.pack(side="right", fill="y");
treeview_lista_obiektow.pack(side="left", expand=True, fill="both")
list_buttons_frame = Frame(ramka_lista_obiektow);
list_buttons_frame.pack(pady=5, fill=X, padx=5)
button_usun_obiekt = Button(list_buttons_frame, text="Usuń");
button_usun_obiekt.pack(side="left", padx=5)
button_edytuj_obiekt = Button(list_buttons_frame, text="Edytuj");
button_edytuj_obiekt.pack(side="left", padx=5)
filter_entry = Entry(list_buttons_frame, font=('Arial', 9));
filter_entry.pack(side="left", padx=10, fill=X, expand=True)
filter_entry.bind("<KeyRelease>", on_filter_change);
treeview_lista_obiektow.bind("<<TreeviewSelect>>", show_item_details)

# --- ramka_formularz ---
label_formularz = Label(ramka_formularz, text="Formularz", font=("Arial", 12, "bold"));
label_formularz.grid(row=0, column=0, columnspan=2, pady=5)
pad_x_entry, pad_y_entry = 5, 3
label_name = Label(ramka_formularz, text="Nazwa:", anchor="w");
label_name.grid(row=1, column=0, sticky=W, padx=pad_x_entry, pady=pad_y_entry)
entry_name = Entry(ramka_formularz, width=30);
entry_name.grid(row=1, column=1, padx=pad_x_entry, pady=pad_y_entry)
label_location = Label(ramka_formularz, text="Lokalizacja:", anchor="w");
label_location.grid(row=2, column=0, sticky=W, padx=pad_x_entry, pady=pad_y_entry)
entry_location = Entry(ramka_formularz, width=30);
entry_location.grid(row=2, column=1, padx=pad_x_entry, pady=pad_y_entry)
label_hotel_select = Label(ramka_formularz, text="Przypisz do hotelu:", anchor="w");
label_hotel_select.grid(row=3, column=0, sticky=W, padx=pad_x_entry, pady=pad_y_entry)
hotel_combobox = ttk.Combobox(ramka_formularz, state="readonly", width=28);
hotel_combobox.grid(row=3, column=1, padx=pad_x_entry, pady=pad_y_entry)
Label(ramka_formularz, text="Szerokość:", anchor="w").grid(row=4, column=0, sticky=W, padx=pad_x_entry,
                                                           pady=pad_y_entry)
entry_lat = Entry(ramka_formularz, width=30);
entry_lat.grid(row=4, column=1, padx=pad_x_entry, pady=pad_y_entry)
Label(ramka_formularz, text="Długość:", anchor="w").grid(row=5, column=0, sticky=W, padx=pad_x_entry, pady=pad_y_entry)
entry_long = Entry(ramka_formularz, width=30);
entry_long.grid(row=5, column=1, padx=pad_x_entry, pady=pad_y_entry)
label_lat_long_info = Label(ramka_formularz, text="Kliknij na mapie by ustawić położenie",
                            font=("Courier New", 8, "italic"), fg="red");
label_lat_long_info.grid(row=6, column=0, columnspan=2, pady=5)
button_dodaj_obiekt = Button(ramka_formularz, text="Dodaj", font=("Arial", 10, "bold"));
button_dodaj_obiekt.grid(row=7, column=0, columnspan=2, pady=10)

# --- ramka_szczegoly_obiektow ---
label_szczegoly_obiektu = Label(ramka_szczegoly_obiektow, text="Szczegóły obiektu:", font=("Arial", 12, "bold"));
label_szczegoly_obiektu.grid(row=0, column=0, columnspan=8, pady=5)
pad_x_details, pad_y_details = 5, 2
label_szczegoly_name = Label(ramka_szczegoly_obiektow, text="Nazwa/Imię:", font=("Arial", 9, "bold"));
label_szczegoly_name.grid(row=1, column=0, sticky=W, padx=pad_x_details, pady=pad_y_details);

label_szczegoly_name_wartosc = Label(ramka_szczegoly_obiektow, text="....", anchor="w");
label_szczegoly_name_wartosc.grid(row=1, column=1, sticky=W)
Label(ramka_szczegoly_obiektow, text="Miejscowość/Adres:", font=("Arial", 9, "bold")).grid(row=1, column=2, sticky=W,
                                                                                           padx=pad_x_details);
label_szczegoly_location_wartosc = Label(ramka_szczegoly_obiektow, text="....", anchor="w");
label_szczegoly_location_wartosc.grid(row=1, column=3, sticky=W)
Label(ramka_szczegoly_obiektow, text="Szerokość:", font=("Arial", 9, "bold")).grid(row=1, column=4, sticky=W,
                                                                                   padx=pad_x_details);
label_szczegoly_lat_wartosc = Label(ramka_szczegoly_obiektow, text="....", anchor="w");
label_szczegoly_lat_wartosc.grid(row=1, column=5, sticky=W)
Label(ramka_szczegoly_obiektow, text="Długość:", font=("Arial", 9, "bold")).grid(row=1, column=6, sticky=W,
                                                                                 padx=pad_x_details);
label_szczegoly_long_wartosc = Label(ramka_szczegoly_obiektow, text="....", anchor="w");
label_szczegoly_long_wartosc.grid(row=1, column=7, sticky=W)
Label(ramka_szczegoly_obiektow, text="Hotel:", font=("Arial", 9, "bold")).grid(row=2, column=0, sticky=W,
                                                                                          padx=pad_x_details,
                                                                                          pady=pad_y_details);
label_szczegoly_hotel_wartosc = Label(ramka_szczegoly_obiektow, text="....", anchor="w");
label_szczegoly_hotel_wartosc.grid(row=2, column=1, sticky=W)
for i in range(8): ramka_szczegoly_obiektow.grid_columnconfigure(i, weight=1)

# --- ramka_mapa ---
map_widget = tkintermapview.TkinterMapView(ramka_mapa, corner_radius=5);
map_widget.pack(fill="both", expand=True)
map_widget.set_position(52.23, 21.0);
map_widget.set_zoom(6)


# --- czerwony market na mapie pozwalajacy na wybranie pozycji hotelu/goscia/pracownika
def add_marker_on_click(coords):
    map_widget.delete_all_marker();
    entry_lat.delete(0, END);
    entry_lat.insert(0, f"{coords[0]:.4f}")
    entry_long.delete(0, END);
    entry_long.insert(0, f"{coords[1]:.4f}");
    map_widget.set_marker(coords[0], coords[1], text="Wybrano", text_color="red")


map_widget.add_left_click_map_command(add_marker_on_click)


def show_initial_view():
    load_default_test_data() # lista wszystkich hoteli
    setup_filter_placeholder() # filter nazwy hotelu
    notebook_tab_changed(None) # ladowanie zakladki z hotelami


root.after(100, show_initial_view) # po 100 ms zaladuj domyslny widok
root.bind("<Escape>", handle_escape_key) # wscisniecie klawisza escape powoduje powrot to calej listy hoteli/gosci/pracownikow
root.mainloop()

import sqlite3
import tkinter as tk
from tkinter import *
from tkinter import messagebox

#funktsioon mis võtab andmebaasist tabeli
def loe_andmed(yhendus):
    paring = yhendus.execute('SELECT id, first_name, last_name, email, car_make, car_model, car_year, car_price FROM agolubevs')
    andme_list = []
    for rida in paring:
        andme_list.append(rida)
    return andme_list

#otsimisriba 
def otsi(otsisona, loend, yhendus):
    otsisona = otsisona.lower()
    loend.delete(0, END)
    paring = yhendus.execute('SELECT id, first_name, last_name, email, car_make, car_model, car_year, car_price FROM agolubevs')
    for rida in paring:
        if any(otsisona in str(veerg).lower() for veerg in rida):
            loend.insert(END, f"ID: {rida[0]}, Nimi: {rida[1]} {rida[2]}, Email: {rida[3]}, Auto: {rida[4]} {rida[5]}, Aasta: {rida[6]}, Hind: {rida[7]}")

#nuppud lehekylje vahetamiseks
def lehekuljenupud(aken, praegune, lehearv, loend):
    eelmine = Button(aken, text="Eelmine lehekülg", command=lambda: vahetamine(aken, praegune - 1, lehearv, loend), state=DISABLED if praegune == 0 else NORMAL)
    eelmine.grid(row=3, column=0, pady=10)
    järgmine = Button(aken, text="Järgmine lehekülg", command=lambda: vahetamine(aken, praegune + 1, lehearv, loend), state=DISABLED if praegune == lehearv - 1 else NORMAL)
    järgmine.grid(row=3, column=1, pady=10)

#funktsioon andme kustutamiseks
def kustuta_andmed(id, loend):
    yhendus = sqlite3.connect('epood_agolubevs.db')
    yhendus.execute('DELETE FROM agolubevs WHERE id=?', (id,))
    yhendus.commit()
    yhendus.close()
    laadi_uuesti(loend)

#funktsioon mis kustutab kasutaja anedmebaasist
def laadi_uuesti(loend):
    loend.delete(0, END)
    andme_list = loe_andmed(sqlite3.connect('epood_agolubevs.db'))
    kuvatudandmed(andme_list, loend)

#lehekylje vahetamine funktsioon
def vahetamine(aken, uus, lehearv, loend):
    global andme_list
    uus = max(0, min(uus, lehearv - 1))
    loend.delete(0, END)
    andme_list = loe_andmed(sqlite3.connect('epood_agolubevs.db'))
    kuvatudandmed(kuvatud_andmed(andme_list, uus, lehearv), loend)
    lehekuljenupud(aken, uus, lehearv, loend)


def kuvatud_andmed(andme_list, lehekylg, andmed_igal_lehel):
    algus = lehekylg * andmed_igal_lehel
    lopp = min(algus + andmed_igal_lehel, len(andme_list))
    return andme_list[algus:lopp]

def kuvatudandmed(andmed, loend):
    for andmed_rida in andmed:
        loend.insert(END, f"ID: {andmed_rida[0]}, Nimi: {andmed_rida[1]} {andmed_rida[2]}, Email: {andmed_rida[3]}, Auto: {andmed_rida[4]} {andmed_rida[5]}, Aasta: {andmed_rida[6]}, Hind: {andmed_rida[7]}")

#funktsioon andme lisamiseks
def andmelisamine(aken, yhendus, loend):
    def lisa_andmed():
        first_name = eesnimi_entry.get()
        last_name = perenimi_entry.get()
        email = email_entry.get()
        car_make = automark_entry.get()
        car_model = automudel_entry.get()
        car_year = aasta_entry.get()
        car_price = hind_entry.get()

        if first_name and last_name and email and car_make and car_model and car_year and car_price:
            try:
                yhendus.execute("INSERT INTO agolubevs (first_name, last_name, email, car_make, car_model, car_year, car_price) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (first_name, last_name, email, car_make, car_model, car_year, car_price))
                yhendus.commit()
                loend.delete(0, END)
                andme_list = loe_andmed(yhendus)
                kuvatudandmed(andme_list, loend)
                messagebox.showinfo("Edukalt lisatud", "Andmed on edukalt lisatud andmebaasi.")
            except Exception as e:
                messagebox.showerror("Viga", f"Andmete lisamisel tekkis viga: {e}")
        else:
            messagebox.showerror("Puuduvad väljad", "Palun täitke kõik väljad.")
    #uus aken andmete lisamiseks
    andmelisamise_aken = Toplevel(aken)
    andmelisamise_aken.title("Lisa uued andmed")
    andmelisamise_aken.geometry("400x300")

    silt = Label(andmelisamise_aken, text="Lisa uued andmed:")
    silt.grid(row=0, column=0, columnspan=2, pady=10)

    eesnimi_silt = Label(andmelisamise_aken, text="Eesnimi:")
    eesnimi_silt.grid(row=1, column=0, padx=10, pady=5)
    eesnimi_entry = Entry(andmelisamise_aken)
    eesnimi_entry.grid(row=1, column=1, padx=10, pady=5)

    perenimi_silt = Label(andmelisamise_aken, text="Perenimi:")
    perenimi_silt.grid(row=2, column=0, padx=10, pady=5)
    perenimi_entry = Entry(andmelisamise_aken)
    perenimi_entry.grid(row=2, column=1, padx=10, pady=5)

    email_silt = Label(andmelisamise_aken, text="Email:")
    email_silt.grid(row=3, column=0, padx=10, pady=5)
    email_entry = Entry(andmelisamise_aken)
    email_entry.grid(row=3, column=1, padx=10, pady=5)

    automark_silt = Label(andmelisamise_aken, text="Auto mark:")
    automark_silt.grid(row=4, column=0, padx=10, pady=5)
    automark_entry = Entry(andmelisamise_aken)
    automark_entry.grid(row=4, column=1, padx=10, pady=5)

    automudel_silt = Label(andmelisamise_aken, text="Auto mudel:")
    automudel_silt.grid(row=5, column=0, padx=10, pady=5)
    automudel_entry = Entry(andmelisamise_aken)
    automudel_entry.grid(row=5, column=1, padx=10, pady=5)

    aasta_silt = Label(andmelisamise_aken, text="Auto aasta:")
    aasta_silt.grid(row=6, column=0, padx=10, pady=5)
    aasta_entry = Entry(andmelisamise_aken)
    aasta_entry.grid(row=6, column=1, padx=10, pady=5)

    hind_silt = Label(andmelisamise_aken, text="Auto hind:")
    hind_silt.grid(row=7, column=0, padx=10, pady=5)
    hind_entry = Entry(andmelisamise_aken)
    hind_entry.grid(row=7, column=1, padx=10, pady=5)

    lisa_nupp = Button(andmelisamise_aken, text="Lisa andmed", command=lisa_andmed)
    lisa_nupp.grid(row=8, column=0, columnspan=2, pady=10)


#graafiline aken
def graafiline():
    aken = tk.Tk()
    aken.title("SQLite andmebaas")
    aken.geometry("1000x800")

    yhendus = sqlite3.connect('epood_agolubevs.db')

    silt = Label(aken, text="Andmed:")
    silt.grid(row=0, column=0)

    loend = Listbox(aken, height=10, width=150)
    loend.grid(row=1, column=0, columnspan=2)

    kerimine = Scrollbar(aken, orient=VERTICAL)
    kerimine.grid(row=1, column=2, sticky="ns")
    kerimine.configure(command=loend.yview)

    loend.configure(yscrollcommand=kerimine.set)

    otsiaken = Entry(aken, width=50)
    otsiaken.grid(row=2, column=0, padx=10, pady=10)

    otsinupp = Button(aken, text="Otsi", command=lambda: otsi(otsiaken.get(), loend, yhendus))
    otsinupp.grid(row=2, column=1)

    lisa_nupp = Button(aken, text="Lisa uued andmed", command=lambda: andmelisamine(aken, yhendus, loend))
    lisa_nupp.grid(row=3, column=0, columnspan=2, pady=10)

    Label(aken, text="Sisesta ID, mida soovite kustutada:").place(x=250, y=300)
    id_sisend = Entry(aken)
    id_sisend.place(x=440, y=300)

    kustuta_nupp = Button(aken, text="Kustuta", command=lambda: kustuta_andmed(id_sisend.get(), loend))
    kustuta_nupp.place(x=570, y=300)

    andme_list = loe_andmed(yhendus)
    andmed_lehel = len(andme_list) // 300 + 1
    praegune_lehekylg = 0
    kogulehearv = 300

    kuvatudandmed(kuvatud_andmed(andme_list, praegune_lehekylg, kogulehearv), loend)
    lehekuljenupud(aken, praegune_lehekylg, kogulehearv, loend)

    aken.mainloop()
    yhendus.close()

graafiline()
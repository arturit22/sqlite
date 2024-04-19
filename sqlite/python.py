import sqlite3
import tkinter as tk
from tkinter import *

def loe_andmed(yhendus):
    paring = yhendus.execute('SELECT id, first_name, last_name, email, car_make, car_model, car_year, car_price FROM agolubevs')
    andme_list = []
    for rida in paring:
        andme_list.append(rida)
    return andme_list

def otsi(otsisona, loend, yhendus):
    otsisona = otsisona.lower()
    loend.delete(0, END)
    paring = yhendus.execute('SELECT id, first_name, last_name, email, car_make, car_model, car_year, car_price FROM agolubevs')
    for rida in paring:
        if any(otsisona in str(veerg).lower() for veerg in rida):
            loend.insert(END, f"ID: {rida[0]}, Nimi: {rida[1]} {rida[2]}, Email: {rida[3]}, Auto: {rida[4]} {rida[5]}, Aasta: {rida[6]}, Hind: {rida[7]}")

def lehekuljenupud(aken, praegune, lehearv, loend):
    eelmine = Button(aken, text="Eelmine lehekülg", command=lambda: vahetamine(aken, praegune - 1, lehearv, loend), state=DISABLED if praegune == 0 else NORMAL)
    eelmine.grid(row=3, column=0, pady=10)
    järgmine = Button(aken, text="Järgmine lehekülg", command=lambda: vahetamine(aken, praegune + 1, lehearv, loend), state=DISABLED if praegune == lehearv - 1 else NORMAL)
    järgmine.grid(row=3, column=1, pady=10)

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


def andmetelisamine():
    lisaken = tk.Topleve()
    lisaken.title("Andmete lisamine")
    lisaken.geometry("400x200")




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

    andme_list = loe_andmed(yhendus)
    andmed_lehel = len(andme_list) // 300 + 1
    praegune_lehekylg = 0
    kogulehearv = 300

    kuvatudandmed(kuvatud_andmed(andme_list, praegune_lehekylg, kogulehearv), loend)
    lehekuljenupud(aken, praegune_lehekylg, kogulehearv, loend)

    aken.mainloop()
    yhendus.close()

graafiline()

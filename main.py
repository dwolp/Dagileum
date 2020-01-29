from datetime import *
from math import *

today = datetime.now()
datadict = {}
selection = ''


def add_birthday():
    new_entry_name = str(input("Skriv inn et navn: "))
    entered_date = str(input("Skriv inn en dato: "))
    new_entry_date = convert_to_datetime(entered_date)
    datadict[new_entry_name] = new_entry_date
    save_to_file()


def open_and_create():
    # open file and create dictionary
    data = open("data.txt", "r")
    for line in data:
        x = line.split(";")
        x[1] = x[1].rstrip("\n")
        datadict[x[0]] = convert_to_datetime(x[1])
    data.close()


def convert_to_datetime(x):
    # input DD.MM.YYYY and return datetime
    new_date = x.split(".")
    new_date = datetime.fromisoformat(new_date[2] + "-" + new_date[1] + "-" + new_date[0])
    return new_date


def print_days_old():
    print("           Navn |  Fødselsdag |  År |  Dager | Neste dagileum ")
    print("       " + "*"*80)
    for people in datadict:
        date_born = datadict[people].strftime("%d.%m.%Y")
        days_old = (today - datadict[people]).days
        years = floor(days_old / 365)
        days_next = (floor(days_old/1000)+1)*1000
        date_next = (today + timedelta(days_next - days_old)).strftime("%d.%m.%Y")
        print(f"{people:>15} | {date_born:>11} | {years:>3} | {days_old:>6} | "
              f"{people} blir {days_next} dager den {date_next}")


def delete_entry():
    print("deleted")


def save_to_file():
    print("")


def check_input():
    print("")


open_and_create()

while selection != "q":
    print(f"\nMeny: (1) Vis  (2) Legg til  (3) Slett  (4) Avslutt")
    selection = input("Ditt valg: ").lower()
    if selection == "legg til" or selection == "2":
        add_birthday()
    elif selection == "vis" or selection == "1":
        print_days_old()
    elif selection == "slett" or selection == "3":
        delete_entry()
    elif selection == "avslutt" or selection == "4":
        print("Ha det bra..")
        break
    else:
        print("Prøv igjen..")

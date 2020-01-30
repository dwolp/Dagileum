from datetime import *
from math import *
import os
import time

today = datetime.now()
datadict = {}
selection = ''
calendardict = {}


def clear():
    os.system('cls')


def add_birthday():
    # adds an entry
    new_entry_name = str(input(" Skriv inn et navn: ")).lower()
    entered_date = ''
    
    while len(entered_date) != 10:
        entered_date = str(input(" Skriv inn en dato: "))
        if len(entered_date) != 10:
            print(" Vennligst bruk formen DD.MM.ÅÅÅÅ")
                  
    new_entry_date = convert_to_datetime(entered_date)
    datadict[new_entry_name] = new_entry_date
    save_to_file()
    print_days_old()


def open_and_create():
    # open file and create dictionary
    data = open("data.txt", "r")
    for line in data:
        x = line.split(";")
        x[1] = x[1].rstrip("\n")
        datadict[x[0].lower()] = convert_to_datetime(x[1])
    data.close()


def convert_to_datetime(x):
    # input DD.MM.YYYY and return datetime
    new_date = x.split(".")
    new_date = datetime.fromisoformat(new_date[2] + "-" + new_date[1] + "-" + new_date[0])
    return new_date


def print_days_old():
    # prints header and the whole table
    clear()
    print(" ")
    print("           Navn |  Fødselsdag |  År |  Dager | Neste dagileum ")
    print("       " + "*" * 80)
    for people in datadict:       
        date_born = datadict[people].strftime("%d.%m.%Y")
        days_old = (today - datadict[people]).days
        years = floor(days_old / 365)
        days_next = (floor(days_old / 1000) + 1) * 1000
        date_next = (today + timedelta(days_next - days_old)).strftime("%d.%m.%Y")
        date_next_for_cal = (today + timedelta(days_next - days_old)).strftime("%Y%m%d")
        print(f"{people.capitalize():>15} | {date_born:>11} | {years:>3} | {days_old:>6} | "
              f"{people.capitalize()} blir {days_next} dager den {date_next}")
        make_calendar_dict(people, days_next, date_next_for_cal)


def delete_entry():
    # deletes an entry
    delete_this = input(" Hvem vil du slette?: ").lower()
    if delete_this in datadict:
        datadict.pop(delete_this)
    else:
        print(" Denne finnes ikke.")
        time.sleep(0.4)
    print_days_old()


def save_to_file():
    # open file and save dictionary
    data = open("data.txt", "w")
    for people in datadict:
        date_born = datadict[people].strftime("%d.%m.%Y")
        data.write(f"{people};{date_born}\n")
    data.close()

    
def export_to_calendar():
    # creates an ICS-file that can be imported to any calendar
    calfile = open("dagileum.ics", "w")
    calfile.write(f"BEGIN:VCALENDAR\n")
    for people in calendardict:
        calfile.append(f"BEGIN:VEVENT\n")
        calfile.append(f"DTSTART:{calendardict[people][2]}\n")
        calfile.append(f"DTEND:{calendardict[people][2]}\n")
        calfile.append(f"SUMMARY:{calendardict[people][0]} {calendardict[people][1]} dager \n")
        calfile.append(f"END:VEVENT\n")
    calfile.append(f"END:VCALENDAR")
    calfile.close()


def make_calendar_dict(name, days, date):
    calendardict[name] = [name, days, date]
    

# program starts here

open_and_create()


while selection != 'q':
    print(f"\n Meny: (1) Vis  (2) Legg til  (3) Slett  (4) Avslutt")
    selection = input(" Ditt valg: ").lower()
    if selection == "legg til" or selection == "2":
        add_birthday()
    elif selection == "vis" or selection == "1":
        print_days_old()
    elif selection == "slett" or selection == "3":
        delete_entry()
    elif selection == "avslutt" or selection == "4":
        print(" Ha det bra..")
        time.sleep(1)
        break
    else:
        print(" Prøv igjen..")

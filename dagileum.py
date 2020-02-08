import os
from time import sleep as sleep_for
from datetime import *
from math import *
import pickle

today = datetime.now()
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
    pickle_data(datadict)
    print_days_old()


def pickle_data(x):
    outfile = open('data', 'wb')
    pickle.dump(x, outfile)
    outfile.close()


def unpickle_data(x):
    infile = open(x, 'rb')
    x = pickle.load(infile)
    infile.close()
    return x 


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
        make_calendar_dict(people.capitalize(), days_next, date_next_for_cal)


def delete_entry():
    # deletes an entry
    delete_this = input(" Hvem vil du slette?: ").lower()
    if delete_this in datadict:
        datadict.pop(delete_this)
    else:
        print(" Denne finnes ikke.")
        sleep_for(2)
    pickle_data(datadict)
    print_days_old()

    
def export_to_calendar():
    # creates an ICS-file that can be imported to any calendar
    calfile = open("dagileum.ics", "w")
    calfile.write(f"BEGIN:VCALENDAR\n")
    calfile.close()    
    calfile = open("dagileum.ics", "a")
    for people in calendardict:
        calfile.write(f"BEGIN:VEVENT\n")
        calfile.write(f"DTSTART:{calendardict[people][2]}\n")
        calfile.write(f"DTEND:{calendardict[people][2]}\n")
        calfile.write(f"SUMMARY:{calendardict[people][0]} {calendardict[people][1]} dager \n")
        calfile.write(f"END:VEVENT\n")
    calfile.write(f"END:VCALENDAR")
    calfile.close()
    print(f" OK! .ics-fil er opprettet..")
    sleep_for(3)
    print_days_old()


def make_calendar_dict(name, days, dato):
    calendardict[name] = [name, days, dato]
    

# program starts here

datadict = unpickle_data('data')


while selection != 'q':
    print(f"\n Meny: (1) Vis  (2) Legg til  (3) Eksporter til kalender  (4) Slett  (5) Avslutt")
    selection = input(" Ditt valg: ").lower()
    if selection == "legg til" or selection == "2":
        add_birthday()
    elif selection == "vis" or selection == "1":
        print_days_old()
    elif selection == "slett" or selection == "4":
        delete_entry()
    elif selection == "eksporter" or selection == "3":
        export_to_calendar()
    elif selection == "avslutt" or selection == "5":
        print(" Ha det bra..")
        sleep_for(2)
        break
    else:
        print(" Prøv igjen..")

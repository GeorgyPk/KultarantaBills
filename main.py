from cgitb import small
import PySimpleGUI as sg
import openpyxl
import datetime

class Bill:
    bill_id = ""
    reference_number = ""
    name = ""
    date_bill = ""
    date_arrival = ""
    date_departure = ""
    bed_linen = 0
    cleaning = 0
    night_price_big = 0
    night_price_small = 0
    cottage_count_small = 0
    cottage_count_big = 0
    cottage_numbers = ""
    other_expenses = 0
    total_price = 0

#Function for counting reference number (working)
#Formula for the reference number https://fi.wikipedia.org/wiki/Tilisiirto
def count_reference_number(bill_id):
    multiplier_list = []
    for i in range(0, 30):
        multiplier_list.extend([7, 3, 1])
    list_count = 0
    sum = 0
    for i in reversed(bill_id):
        sum = sum + (int(i) * multiplier_list[list_count])
        list_count += 1
    next_ten = (sum // 10 + (sum % 10 > 0)) * 10
    additional_number = next_ten - sum
    reference_number = f"{bill_id}{additional_number}"
    print("Reference number:", reference_number)
    return reference_number

#Function for getting bill id (working)
def get_bill_id(entered_id):
    if entered_id != 0:
        wfile = open('latestbill.txt', 'w')
        wfile.write(str(entered_id))
        wfile.close()
        return entered_id
    else:
        file = open('latestbill.txt', 'r')
        bill_id = file.readline()
        file.close()
        bill_id = write_next_bill_id(str(bill_id))
        return bill_id

#Figure out next bill_id (working)
def write_next_bill_id(previous_bill_id):
    first_two_chars = previous_bill_id[:2]
    last_characters = previous_bill_id[2:]
    new_bill_id = f"{first_two_chars}{int(last_characters)+1}"
    wfile = open("latestbill.txt", "w")
    wfile.write(new_bill_id)
    wfile.close()
    return new_bill_id

#Function for figuring out prices (working)
def determine_prices(input_price):
    price_list = input_price.split("/")
    small_cottage_price = int(price_list[0])
    big_cottage_price = int(price_list[1])
    if small_cottage_price == 0 or small_cottage_price == 145:
        small_cottage_price = 145
    if big_cottage_price == 0 or big_cottage_price == 195:
        big_cottage_price = 195
    right_prices = [small_cottage_price, big_cottage_price]
    return right_prices

#Get current date (working)
def get_date_today():
    today = datetime.datetime.today()
    bill_obj.date_bill = today.strftime("%d.%m.%Y")

#Count price
def count_cleaning_price(pet, cleaning_count):
    if pet == True:
        cleaning_price = 65 * cleaning_count
    else:
        cleaning_price = 50 * cleaning_count
    return cleaning_price

#Count rent price of the cottages (working)
def count_rent_price(night_price_list, cottage_count_list, arrival, departure):
    arrival = datetime.datetime.strptime(arrival, '%d.%m.%Y')
    departure = datetime.datetime.strptime(departure, '%d.%m.%Y')
    delta = departure - arrival
    nights = delta.days

    bill_obj.night_price_small = night_price_list[0]
    bill_obj.night_price_big = night_price_list[1]

    bill_obj.cottage_count_small = cottage_count_list[0]
    bill_obj.cottage_count_big = cottage_count_list[1]

    #print("Price small:",bill_obj.night_price_small,"\nPrice big:",bill_obj.night_price_big,"\nCottage count small:",bill_obj.cottage_count_small,"\nCottage count big:",bill_obj.cottage_count_big)
    small_cottage_total_price = int(bill_obj.night_price_small) * int(bill_obj.cottage_count_small) * int(nights)
    big_cottage_total_price = int(bill_obj.night_price_big) * int(bill_obj.cottage_count_big) * int(nights)
    total_price = small_cottage_total_price + big_cottage_total_price
    return 0


first_column= [
    [sg.Text("Laskun numero:")],
    [sg.Text("Nimi:")],
    [sg.Text("Saapumispäivä:")],
    [sg.Text("Lähtöpäivä:")],
    [sg.Text("Yöhinta:")],
    [sg.Text("Mökkien määrä:")],
    [sg.Text("Mökkien numerot:")],
    [sg.Text("Liinavaatteet:")],
    [sg.Text("Siivous:")],
    [sg.Text("Muut kulut:")],
    [sg.Button('OK', size = 10, bind_return_key=True)],
]

second_column = [
    [sg.Input(0, size=(25,1), key="-BILL_ID-")],
    [sg.Input("", size=(25,1), key="-NAME-")],
    [sg.Input("", size=(25,1), key="-ARRIVAL_DATE-")],
    [sg.Input("", size=(25,1), key="-DEPARTURE_DATE-")],
    [sg.Input("0/0", size=(25,1), key="-NIGHT_PRICES-")],
    [sg.Input("0/0", size=(25,1), key="-COTTAGE_COUNT-")],
    [sg.Input("mökki #", size=(25,1), key="-COTTAGE_NUMBERS-")],
    [sg.Input(0, size=(25,1), key="-BED_LINEN-")],
    [sg.Input(0, size=(25,1), key="-CLEANING-")],
    [sg.Input(0, size=(25,1), key="-OTHER_EXPENSES-")],
]

third_column= [
    [sg.Text("(0 tai väh. 3 kirjainta)")],
    [sg.Text("")],
    [sg.Text("(dd.mm.yyyy):")],
    [sg.Text("(dd.kk.yyyy):")],
    [sg.Text("(pieni/iso | jätä 0, jos tavallinen hinta)")],
    [sg.Text("(pieni/iso)")],
    [sg.Text("")],
    [sg.Text("(kpl)")],
    [sg.Checkbox("Lemmikki", default=False, key="-PET-")],
    [sg.Text("")],
    [sg.Button("Exit", size = 10)]
]

custom_layout = [[sg.Column(first_column, vertical_alignment="t"), sg.Column(second_column, vertical_alignment="t"), sg.Column(third_column, vertical_alignment="t")]]

window = sg.Window(title="Laskut", layout=custom_layout, margins=(50, 25))

while True:
    event, values = window.read()
    #Exiting the program
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    #Getting all the texts when 'OK' is pressed
    if event == "OK":
        bill_obj = Bill()
        bill_obj.name = values["-NAME-"]
        bill_obj.cottage_numbers = values["-COTTAGE_NUMBERS-"]

        get_date_today()
        bill_obj.bill_id = get_bill_id(int(values["-BILL_ID-"]))
        bill_obj.reference_number = count_reference_number(bill_obj.bill_id)

        night_price_list = determine_prices(values["-NIGHT_PRICES-"])
        cottage_count_list = values["-COTTAGE_COUNT-"].split("/")

        bill_obj.date_arrival = values["-ARRIVAL_DATE-"]
        bill_obj.date_departure = values["-DEPARTURE_DATE-"]

        bill_obj.bed_linen = values["-BED_LINEN-"]
        bill_obj.cleaning = values["-CLEANING-"]
        bill_obj.other_expenses = values["-OTHER_EXPENSES-"]

        #Begin counting total price
        bill_obj.total_price = count_cleaning_price(values["-PET-"], bill_obj.cleaning)
        bill_obj.total_price = bill_obj.total_price + (bill_obj.bed_linen * 15)
        bill_obj.total_price = bill_obj.total_price + bill_obj.other_expenses
        bill_obj.total_price = int(bill_obj.total_price) + int(count_rent_price(night_price_list, cottage_count_list, bill_obj.date_arrival, bill_obj.date_departure))

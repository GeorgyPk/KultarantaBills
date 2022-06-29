import PySimpleGUI as sg
import openpyxl

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
    cottage_numbers = ""
    other_expenses = 0

#Function for counting reference number
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

#Function for getting bill id
def get_bill_id(entered_id):
    if entered_id != 0:
        return entered_id
    else:
        file = open('latestbill.txt', 'r')
        bill_id = file.readline()
        print("In function:",bill_id)
        #TODO
        return bill_id

#Function for splitting and figuring out prices
def split_and_determine_prices(input_price):
    price_list = input_price.split("/")
    small_cottage_price = price_list[0]
    big_cottage_price = price_list[1]
    if small_cottage_price == 0:
        pass



first_column= [
    [sg.Text("Laskun numero:")],
    [sg.Text("Nimi:")],
    [sg.Text("Saapumispäivä (dd.mm.yyyy):")],
    [sg.Text("Lähtöpäivä (dd.kk.yyyy):")],
    [sg.Text("Yöhinta (pieni/iso | jätä 0, jos tavallinen hinta):")],
    [sg.Text("Mökkien määrä (pieni/iso):")],
    [sg.Text("Mökkien numerot:")],
    [sg.Text("Liinavaatteet (kpl):")],
    [sg.Text("Siivous (Määrä):")],
    [sg.Text("Muut kulut:")],
    [sg.Button('OK', size = 10)],
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
    [sg.Button("Exit", size = 10)]
]

custom_layout = [[sg.Column(first_column),sg.Column(second_column)],]

window = sg.Window(title="Laskut", layout=custom_layout, margins=(50, 25))

while True:
    event, values = window.read()
    #Exiting the program
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    #Getting all the texts when 'OK' is pressed
    if event == "OK":
        bill_obj = Bill()
        bill_obj.bill_id = get_bill_id(int(values["-BILL_ID-"]))
        bill_obj.name = values["-NAME-"]
        bill_obj.date_arrival = values["-ARRIVAL_DATE-"]
        bill_obj.date_departure = values["-DEPARTURE_DATE-"]
        bill_obj.bed_linen = values["-BED_LINEN-"]
        bill_obj.cleaning = values["-CLEANING-"]
        bill_obj.other_expenses = values["-OTHER_EXPENSES-"]

        night_price_list = split_and_determine_prices(values["-NIGHT_PRICES-"])

        print("Out of function:",bill_obj.bill_id)

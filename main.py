import PySimpleGUI as sg
import openpyxl

class Bill:
    bill_id = ""
    reference_number = ""
    name = ""
    date_bill = ""
    date_rent_start = ""
    date_rent_end = ""
    bed_linen = 0
    cleaning = 0
    night_cost = 0
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
    return reference_number



#sg.Window(title="Laskut", layout=[[]], margins=(100, 50)).read()
import Menus
import Prints

class main:
    choise = '0'
    Prints.Prints.menu()
    while choise not in ["1","2"]:
        choise = input("Please choose your option: ")
    if choise == '1':
        Menus.MenusRecon.main_recon()
    if choise == '2':
        Menus.MenusScan.main_scan()
    else:
        print("Bad Input Exiting...")
        exit()
    
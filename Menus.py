import Prints
import Recon
import Scan
import Misc 

class MenusRecon:        
    def main_recon():
        try:
            choise = '0'
            Misc.Misc.clear_screen()
            Prints.Prints.print_menu_recon()
            while choise not in "12345":
                choise = input("Please choose your option: ")
            path = Misc.Misc.make_dir("Recon")
            Recon.Recon.init_scanner(choise, path)
            input("\npress enter to exit")
        except KeyboardInterrupt:
            Misc.Misc.clear_screen()
            print(f"\nBye See You Never :D\n")

class MenusScan: 
    def main_menu():
        choise = '0'
        Misc.Misc.clear_screen()
        Prints.Prints.print_menu_scan()
        while choise not in "12":
                choise = input("Please choose your option: ")
        if choise == '1':
            Scan.ScanInit.print_res(Scan.ScanInit.arp_nmap())
        elif choise == '2':
            MenusScan.socket_scan()
        else:
            Misc.Misc.clear_screen()
            print("Bad Input!!! Exiting")
            exit()
        
    def socket_scan():
        choise = '0'
        Misc.Misc.clear_screen()
        Prints.Prints.print_socket_scan()
        while choise not in "12":
                choise = input("Please choose your option: ")
        if choise == '1':
            Scan.ScanInit.print_res(Scan.ScanInit.arp_socket("fast"))
        elif choise == '2':
            Scan.ScanInit.print_res(Scan.ScanInit.arp_socket("full"))

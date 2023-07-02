import Prints
import Recon
import Scan
import Misc

class MenusRecon:        
    def main_recon():
        try:
            choise = '0'
            Misc.Tools.clear_screen()
            Prints.Prints.print_menu_recon()
            while choise not in ["1","2","3","4","5"]:
                choise = input("Please choose your option: ")
            path = Misc.Tools.make_dir("Recon")
            Recon.Recon.init_scanner(choise, path)
            input("\npress enter to exit")
        except KeyboardInterrupt:
            Misc.Tools.clear_screen()
            print(f"\nBye See You Never :D\n")

class MenusScan: 
    def main_scan():
        choise = '0'
        Misc.Tools.clear_screen()
        Prints.Prints.print_menu_scan()
        while choise not in ["1","2"]:
                choise = input("Please choose your option: ")
        if choise == '1':
            Scan.ScanInit.print_res(Scan.ScanInit.arp_nmap())
        elif choise == '2':
            MenusScan.socket_scan()
        else:
            Misc.Tools.clear_screen()
            print("Bad Input!!! Exiting")
            exit()
        
    def socket_scan():
        choise = '0'
        Misc.Tools.clear_screen()
        Prints.Prints.print_socket_scan()
        while choise not in ["1","2"]:
                choise = input("Please choose your option: ")
        if choise == '1':
            Scan.ScanInit.print_res(Scan.ScanInit.arp_socket("fast"))
        elif choise == '2':
            Scan.ScanInit.print_res(Scan.ScanInit.arp_socket("full"))

class MiscTools:
    def misc_menu():
        choise = '0'
        Prints.Prints.print_misc_tools()
        while choise not in ["1","2","3","4"]:
            choise = input()
            if choise == '1':
                Misc.ArpScanner.main()
            if choise == '2':
                Misc.PingSweep.main()
            if choise == '3':
                Misc.KernalCVEs.main()
            if choise == '4':
                Misc.BasicPortScanner.main()
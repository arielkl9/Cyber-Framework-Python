import Misc

class Prints:
    def menu():
        Misc.Misc.clear_screen()
        print("Welcome To My Framework!!\n")
        print("This Program Is Still In Development\n")
        print("Please Choose Module:\n")
        print("1. Recon Module\n")
        print("2. Scan Module\n")

    def print_menu_recon():
        Misc.Misc.clear_screen()
        print("\n              Welcome To My Recon Module                \n")
        print("**********************************************************\n")
        print("|                                                        |\n")
        print("|    Options:                                            |\n")
        print("|    [1] Whois Check                                     |\n")
        print("|    [2] DNS Enumeration                                 |\n")
        print("|    [3] Subdomains BF                                   |\n")
        print("|    [4] Directories BF                                  |\n")
        print("|    [5] Everything!!                                    |\n")
        print("|                                                        |\n")
        print("**********************************************************\n")

    def print_menu_scan():
        Misc.Misc.clear_screen()
        print("\n                 Welcome To My Scanning Module                  \n")
        print("*******************************************************************\n")
        print("|                                                                 |\n")
        print("|    Options:                                                     |\n")
        print("|    [1] Scan network/ip with ARP & Nmap (Require Nmap installed) |\n")
        print("|    [2] Scan network/ip with ARP & Socket (No requirements)      |\n")
        print("|                                                                 |\n")
        print("*******************************************************************\n")

    def print_socket_scan():
        print("why people insist to go the hard way... anyways...\n")
        print("What scan you want to use?\n")
        print("1. Fast scan - scans only common ports\n")
        print("2. Full scan - scans ALL ports (might take some time)\n")

    
    


    
        
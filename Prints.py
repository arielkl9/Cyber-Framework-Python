import Misc

class Prints:
    def menu():
        Misc.Tools.clear_screen()
        print(
r'''
     _____                                   
    |  ___|  _ __    __ _   _ __ ___     ___ 
    | |_    | '__|  / _` | | '_ ` _ \   / _ \
    |  _|   | |    | (_| | | | | | | | |  __/
    |_|_    |_| __  \__,_| |_| |_| |_|  \___|
       \ \      / /   ___    _ __  | | __     
        \ \ /\ / /   / _ \  | '__| | |/ /     
         \ V  V /   | (_) | | |    |   <      
          \_/\_/     \___/  |_|    |_|\_\     
                                          
'''
        )
        print("**********************************************************\n")
        print("|                                                        |\n")
        print("|    Modules:                                            |\n")
        print("|    [1] Recon Module                                    |\n")
        print("|    [2] Scan Module                                     |\n")
        print("|    [3] Misc Tools                                      |\n")
        print("|                                                        |\n")
        print("**********************************************************\n")

    def print_menu_recon():
        Misc.Tools.clear_screen()
        print(
r'''
         ____                                
        |  _ \    ___    ___    ___    _ __  
        | |_) |  / _ \  / __|  / _ \  | '_ \ 
        |  _ <  |  __/ | (__  | (_) | | | | |
        |_| \_\  \___|  \___|  \___/  |_| |_|       
''')
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
        Misc.Tools.clear_screen()
        print(
r'''
     ____                                   _                 
    / ___|    ___    __ _   _ __    _ __   (_)  _ __     __ _ 
    \___ \   / __|  / _` | | '_ \  | '_ \  | | | '_ \   / _` |
     ___) | | (__  | (_| | | | | | | | | | | | | | | | | (_| |
    |____/   \___|  \__,_| |_| |_| |_| |_| |_| |_| |_|  \__, |
                                                         ___/ 
'''
        )
        print("*******************************************************************\n")
        print("|                                                                 |\n")
        print("|    Options:                                                     |\n")
        print("|    [1] Scan network/ip with ARP & Nmap (Require Nmap installed) |\n")
        print("|    [2] Scan network/ip with ARP & Socket (No requirements)      |\n")
        print("|                                                                 |\n")
        print("*******************************************************************\n")

    def print_socket_scan():
        Misc.Tools.clear_screen()
        print("*******************************************************************\n")
        print("|                                                                 |\n")
        print("|    What scan you want to use?                                   |\n")
        print("|                                                                 |\n")
        print("|    Options:                                                     |\n")
        print("|    [1] Fast scan - scans only common ports                      |\n")
        print("|    [2] Full scan - scans ALL ports (might take some time)       |\n")
        print("|                                                                 |\n")
        print("*******************************************************************\n")

    def print_misc_tools():
        Misc.Tools.clear_screen()
        print("*******************************************************************\n")
        print("|                                                                 |\n")
        print("|    Choose Tool                                                  |\n")
        print("|                                                                 |\n")
        print("|    Options:                                                     |\n")
        print("|    [1] Arp Scanner                                              |\n")
        print("|    [2] Ping Sweeper                                             |\n")
        print("|    [3] Basic Port Scanner (socket)                              |\n")
        print("|    [4] Kernal CVE's Auto Scan                                   |\n")
        print("|                                                                 |\n")
        print("*******************************************************************\n")
    
    
    


    
        
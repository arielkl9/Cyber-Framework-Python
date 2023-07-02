import os
import subprocess
import datetime
from scapy.all import ARP, Ether, srp
import ipaddress
from icmplib import ping

# This class perform misc tasks
# 
# vars - None
# 
# funcs - clear_screen
# 
# input - None
# 
# output - None

class Tools:
    def clear_screen():
        try:
            os.getuid()
            subprocess.run("clear",shell=True)
        except AttributeError:
            subprocess.run("cls",shell=True)
    
    def make_dir(folder):
        try:
            cwd = os.getcwd()
            time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            path = f"{cwd}/Results/{folder}_Results/{time}"
            os.makedirs(path,exist_ok=True)
            return path
        except Exception:
            Tools.clear_screen()
            print("Error:\n")
            print("Creating Folders Failed!\n")
            print("Press Enter To Exit...\n")
            input()
            exit()

class ArpScanner:
    def arp_conf():
        while True:
            try:
                ArpScanner.clear_screen()
                get_input = input("pls enter ip range (CIDR Format: x.x.x.x/x): ")
                ip_range = ipaddress.ip_network(get_input)
                arp_request = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_range.compressed)
                return arp_request
            except ValueError or AttributeError:
                continue

    def scan():
        arp_request = ArpScanner.arp_conf()
        answer, unanswered = srp(arp_request, timeout=2)
        return answer
            
    def data_managment():
            answer = ArpScanner.scan()
            for snd, rcv in answer:
                host = {
                    'ip' : rcv.sprintf('%ARP.psrc%'),
                    'mac' : rcv.sprintf('%Ether.src%')
                    }
                alive_hosts.append(host)

    def log():
        path = Tools.make_dir("Arp_Scan")
        with open(f"{path}/Arp_Scan.txt","w") as file:
            file.write(f"Scan Result: \n\nAlive Hosts: \n")
            for i in range(len(alive_hosts)):
                file.write(f"{alive_hosts[i]['ip']} - {alive_hosts[i]['mac']}\n")

    def clear_screen():
        try:
            os.getuid()
            subprocess.run("clear",shell=True)
        except AttributeError:
            subprocess.run("cls",shell=True)

    def main():
        global alive_hosts
        alive_hosts = []
        ArpScanner.data_managment()
        ArpScanner.log()

class PingSweep:
    def get_ip_range():
        ip_range = input("pls enter ip range (x.x.x.x/x)")
        return str(ip_range)
    
    def ping_loop():
        ip_range = PingSweep.get_ip_range()
        while True:
            try:
                for i in ipaddress.IPv4Network(ip_range):
                    a = ping(str(i), count=1, interval=1, timeout=0.1, id=None, source=None, family=None, privileged=True)
                    if "Packets received: 1" in str(a):
                        print(f"{str(i)} is alive!")
                        devices['alive'].append(str(i))
                    else:
                        print(f"{str(i)} is dead!")
                        devices['dead'].append(str(i))
                break
            except Exception as e:
                print(f"{e}\nTry Again Pls")
                continue

    def results():
        path = Tools.make_dir("Ping_Sweeper")
        with open(f"{path}/Ping_Sweeper.txt","w") as file:
            file.write("Ping Sweep Result:\n\n")
            if devices["alive"]:
                file.write("Alive IPs:\n")
                for i in devices["alive"]:
                    file.write(f"{i}\n")
            file.write("\n")
            if devices["dead"]:
                file.write("Dead IPs:\n")
                for i in devices["dead"]:
                    file.write(f"{i}\n")
    def main():
        global devices
        devices = {
            'alive' : [],
            'dead' : []
        }
        Tools.clear_screen()
        PingSweep.ping_loop()
        PingSweep.results()
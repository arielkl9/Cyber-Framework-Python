import os
import subprocess
import datetime
from scapy.all import ARP, Ether, srp
import ipaddress
from icmplib import ping
import nmap3
import requests
import time
import re
import json
import socket

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
        with open(f"{path}/Results.txt","w") as file:
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

class KernalCVEs:
    def set_globals():
        path = Tools.make_dir("CVE's_Scan")
        global nmap 
        global nmap_array

        nmap = nmap3.Nmap()
        nmap_array = []

        global nmap_file
        global json_file
        global cve_file
        global scan_file  
        
        nmap_file = open(f"{path}/nmap_scan.json","w")
        json_file = open(f"{path}/results.json","w")
        cve_file = open(f"{path}/CVE's_found.txt","w")
        scan_file = open(f"{path}/readable.txt","w")

    def get_hosts():
        while True:
            try:
                hosts = ipaddress.IPv4Network(input("Enter Network To Scan (Format CIDR -> X.X.X.X/X): "))
                break
            except Exception:
                Tools.clear_screen()
                continue
        return hosts

    def scan_managment():
        hosts = KernalCVEs.get_hosts()
        json_data = {}
        for ip in hosts:
            dic, readable_format = KernalCVEs.scan(ip.compressed)
            if dic:
                dic = KernalCVEs.check_cve(dic)
                json_data[f'{ip}'] = KernalCVEs.log(ip.compressed,readable_format, dic)
        json_file.writelines(json.dumps(json_data,indent=2))

    def scan(host):
        Tools.clear_screen()
        try:
            print(f"\nScannning {host}...\n")
            dic = {}
            readable_format = []
            data = nmap.nmap_version_detection(host)
            if data[f"{host}"]['ports']:
                dic = data[f"{host}"]['ports']
                nmap_array.append(data)
                scan_file.writelines(f"\nScan Result For {host}:\n")
                for port in data[f"{host}"]['ports']:
                    try:
                        text = ""
                        text += f"Protocol -> {port['protocol']} | Port -> {port['portid']} | Service Data -> "
                        service = port['service'].keys()      
                        for item in service:
                            text += f"{port['service'][item]} "
                        text += f" | CPE -> {port['cpe'][0]['cpe']}"
                    except IndexError or KeyError as e:
                        text = ""
                        text += f"Protocol -> {port['protocol']} | Port -> {port['portid']} | Service Data -> "
                        service = port['service'].keys()      
                        for item in service:
                            text += f"{port['service'][item]} "
                        pass
                    scan_file.writelines(f"{text}\n")
                    readable_format.append(text)
                return (dic ,readable_format)
            else:
                return (0, "")
        except ConnectionError:
            return (0, "")


    def check_cve(dic):
        if dic:
            print("Host Alive!\n")
            print("Checking CVE's...\n")
            print("Using API May Take Some Time...\n")
            for i in range(len(dic)):
                try:
                    for item in dic[i]['cpe']:
                        cve_list = []
                        cpe = item['cpe'].strip("cpe:/")
                        r = requests.get(f'https://services.nvd.nist.gov/rest/json/cves/2.0?cpeName=cpe:2.3:{cpe}')
                        cve = re.findall("CVE-\d{4}-\d{4,7}",r.text)
                        if cve:
                            cve = set(cve)
                            for x in cve:
                                cve_list.append(x)
                            dic[i]['cve'] = sorted(cve_list, reverse=True)
                        time.sleep(6)
                except KeyError:
                    continue
            return (dic)
        else:
            return (0)

    def log(ip,readable_format,dic):
        nmap_file.writelines(json.dumps(nmap_array,indent=2))
        cve_file.writelines(f"\nScan Results For Ip - {ip}:\n")
        for i in range(len(dic)):
            cve_file.writelines("--------------------------------------------------------------------------------------------------------\n")
            cve_file.writelines(f"\n\tResult {i+1}:\n\n")
            cve_file.writelines(f"\t\t{readable_format[i]}\n")
            try:
                if dic[i]['cve']:
                    cve_file.writelines(f"\n\t\t\tCVE's Found:\n\n")
                    for cve in dic[i]['cve']:
                        if cve:
                            cve_file.writelines(f'\t\t\t\t{cve}\n')   
                else:
                    cve_file.writelines(f"\t\t\tNo CVE's Found\n\n")
            except KeyError:
                cve_file.writelines(f"\t\t\tNo CVE's Found\n\n")
        cve_file.writelines("--------------------------------------------------------------------------------------------------------\n")
        return dic

    def close_files():
        nmap_file.close()
        json_file.close()
        cve_file.close()
        scan_file.close()

    def main():
        try:
            Tools.clear_screen()
            os.makedirs('results', exist_ok=True)
            KernalCVEs.set_globals()
            KernalCVEs.scan_managment()
            KernalCVEs.close_files()
            
        except KeyboardInterrupt:
            Tools.clear_screen()
            KernalCVEs.close_files()
            print(f"\nExiting")
            exit()

class BasicPortScanner:
    def main():
        try:
            path = Tools.make_dir("Basic_Port_Scanner")
            while True:
                try:
                    Tools.clear_screen()
                    get_target=ipaddress.IPv4Network(input("enter IP to scan: (CIDR Format: x.x.x.x/x) "))
                    break
                except TypeError and ipaddress.AddressValueError and ValueError:
                    pass
            ports = input("Enter port range (Format: port-port)")
            with open(f'{path}/Results.txt','w') as textfile:
                textfile.write(f"The Best Port Scanner In Town!\n\n")
                print(f"The Best Port Scanner In Town!\n")
                for ip in get_target:
                    Tools.clear_screen()
                    try:
                        if str(ip).split(".")[-1] == "0":
                            continue
                        textfile.writelines(f"\n\nScanned Host: {ip}\nPorts Details:\n")
                        print(f"Scanned Host: {ip}\nPort Range {port1}-{port2}\nFormat (port -> banner)\n\nPorts Details:\n\n")
                        port1 = int(ports.split("-")[0])
                        port2 = int(ports.split("-")[1])
                        for port in range(int(f"{port1+1}"),int(f"{port2+1}")):
                            try:
                                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                s.settimeout(1)
                                result = s.connect_ex((ip.compressed,port))
                                if result == 0:
                                    text=f"port {port} is open"
                                    data = s.recv(1024)
                                    print(f"{text} -> {data}")
                                    textfile.write(f"{text} -> {data}\n")
                                s.close()
                            except TimeoutError:
                                print(f"{text}")
                                textfile.write(f"{text}\n")
                                s.close()
                                continue

                    except socket.error as e:
                            print(f"\nServer not responding")
                            print(e)
                            s.close()
                            continue
        except KeyboardInterrupt:
                    print(f"\nExiting")
                    s.close()
                    exit()
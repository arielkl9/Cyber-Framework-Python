import whois
import dns.resolver
import requests
import Misc
import os
from alive_progress import alive_bar
import urllib.request

class Recon:
    def who_is(website, path):
        with open(f"{path}/Whois.txt","w") as whoisfile:
            print("Initializing Whois Scan...\n")
            whoisfile.write("\nWhois Scan Results:\n\n")
            try:
                os.getuid()
                website = website.strip("https://")
                website = website.strip("http://")
                whoisresult = whois.query(website)
                for i in whoisresult.__dict__.keys():
                    whoisfile.writelines(f"{str(i)}:\n")
                    whoisfile.writelines(f"{str(whoisresult.__dict__[i])}\n\n")
                    print(f"{str(i)}:")
                    print(f"{str(whoisresult.__dict__[i])}\n")
                
            except AttributeError:
                whoisresult = whois.whois(website)
                whoisfile.write(str(whoisresult))
                print(f"{whoisresult}\n")

    def dns_enum(website, path):
        website = website.strip("https://")
        website = website.strip("http://")
        with open(f"{path}/DNS_Enum.txt","w") as dnsenumfile:
            print("Initializing DNS Enumeration...\n")
            dnsenumfile.write("DNS Enumeration Results:\n\n")
            record_types = ["A", "AAAA", "CNAME", "MX", "NS", "SOA", "TXT"]
            resolver = dns.resolver.Resolver()
            for record_type in record_types:
                try:
                    answers = resolver.resolve(website, record_type)
                except dns.resolver.NoAnswer:
                    continue
                print(f"{record_type} records for {website}:")
                dnsenumfile.write(f"{record_type} records for {website}:\n")
                for record in answers:
                    print(f"    {record}")
                    dnsenumfile.write(f"    {record}\n")
            print("\n")

    def subdomains(website, path):
        with open(f"{os.getcwd()}/Lists/subdomains.txt","r") as file:
            counter = 0
            for line in file:
                counter += 1
        website = website.split("://")
        with open(f"{path}/Subdomains.txt","w") as subdomainsfile:
            with open(f"Lists/subdomains.txt","r") as listfile:
                with alive_bar(counter) as bar:
                    print("Initializing Subdomain Bruteforce...\n")
                    subdomainsfile.write("Subdomain Bruteforce Results:\n\n")
                    content = listfile.read()
                    subdomains = content.splitlines()
                    discovered_subdomains = []
                    for subdomain in subdomains:
                        url = f"{website[0]}://{subdomain}.{website[1]}"
                        try:
                            requests.get(url,timeout=3.5)
                            print(f"[+] Discovered subdomain: {url}")
                            subdomainsfile.write(f"[+] Discovered subdomain: {url}\n")
                            discovered_subdomains.append(url)
                            bar()
                        except requests.exceptions.ConnectionError:
                            bar()
                            continue
                        except requests.exceptions.InvalidURL:
                            bar()
                            continue

    def dir_buster(website, path): 
        with open(f"{os.getcwd()}/Lists/dirs.txt","r") as file:
            counter = 0
            for line in file:
                counter += 1
        with open(f"{os.getcwd()}/Lists/dirs.txt","r") as file:
            with open(f"{path}/dirs.txt","w") as res:
                with alive_bar(counter) as bar:
                    print("Running Dir Brute Force Abuse...\n")
                    res.writelines("Running Dir Brute Force Abuse...\n\n")
                    print(f"\b\b\b\b\b\b\bUsing List: {os.getcwd()}/Lists/dirs.txt\n\n")
                    res.writelines(f"Using List: {os.getcwd()}/Lists/dirs.txt\n")
                    for line in file:
                        try:
                            line = line.strip("\n")
                            code = urllib.request.urlopen(f'{website}/{line}').getcode()
                            print(f"\b\b\b\b\b\b\b\b[+] {website}/{line} CODE: {code}")
                            res.writelines(f"[+] {website}/{line} CODE: {code}\n")
                            bar()
                        except Exception as e:
                            e = str(e)
                            code = e.split(" ")[2]
                            code = code.strip(":")
                            if code != "404":
                                if code.isnumeric():
                                    print(f"\b\b\b\b\b\b\b\b[+] {website}/{line} CODE: {code}")
                                    res.writelines(f"[+] {website}/{line} CODE: {code}\n")
                            bar()

    def init_scanner(choise, path):
        website = input("\nEnter A Domain To Scan: ")
        Misc.Tools.clear_screen()
        print("\n")
        if choise == '1':
            Misc.Tools.clear_screen()
            Recon.who_is(website, path)
        elif choise == '2':
            Misc.Tools.clear_screen()
            Recon.dns_enum(website, path)
        elif choise == '3':
            Misc.Tools.clear_screen()  
            Recon.subdomains(website, path)
        elif choise == '4':
            Misc.Tools.clear_screen() 
            Recon.dir_buster(website, path)
        elif choise == '5':
            Misc.Tools.clear_screen() 
            Recon.who_is(website, path)
            Recon.dns_enum(website, path)
            Recon.subdomains(website, path)
            Recon.dir_buster(website, path)
        else:
            Misc.Tools.clear_screen() 
            print("bad input!")
            exit()

    
    

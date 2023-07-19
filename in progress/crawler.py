from urllib.parse import urlparse
from bs4 import BeautifulSoup
import concurrent.futures
import subprocess
import requests
import datetime
import time
import json
import os

class Crawler:
    def __init__(self) -> None:
        try:
            self.menu()
            self.good_urls = []
            self.urls_found = []
            self.thread_counter = 0
            self.sites_looked = 0
            self.domain = self.get_domain()
            self.start_time = time.time()
            self.base_domain = self.url.split("://")[-1]
            self.crawl(self.url)
            self.log()
        except KeyboardInterrupt:
            self.clear_screen()
            print("Crawling Interupted!!")
            self.log()

    def __call__(self):
        return "END"

    def crawl(self, url):
        if url not in self.urls_found:
            self.urls_found.append(url)
            with concurrent.futures.ThreadPoolExecutor(max_workers=60) as main_executor:
                html_obj = main_executor.submit(self.get_url,url)
                self.thread_counter += 1
            try:
                if html_obj.result():
                    soup = BeautifulSoup(html_obj.result().text, "html.parser")
                    urls = soup.find_all("a")
                    if urls:
                        with concurrent.futures.ThreadPoolExecutor(max_workers=60) as executor:
                            for a_tag in urls:
                                if a_tag["href"] not in self.urls_found:
                                    executor.submit(self.check_url,a_tag["href"])
                                    self.thread_counter += 1
                                    self.sites_looked += 1
            except Exception:
                pass
        return self.__call__
    
    def check_url(self,url):
        if url and url not in self.good_urls:
            if self.domain in url and "http" in url:
                tld_count = url.count(self.domain)
                if self.base_domain in url and self.scan_type not in url and "#" not in url and tld_count == 1: # "?" not in url and -> only sites
                    self.good_urls.append(url)
                    print(f"{len(self.good_urls)}: {url}\n")
                    return self.crawl(url)
            elif url[0] == "/" and "#" not in url and self.scan_type not in url and f"{self.url}{url}" not in self.good_urls:
                if self.get_url(f"{self.url}{url}"):
                    self.good_urls.append(f"{self.url}{url}")
                    print(f"{len(self.good_urls)}: {self.url}{url}\n")
                    return self.crawl(f"{self.url}{url}")
            
                            
    def get_url(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
                }
            response = requests.get(url, headers, timeout=6)
            if response.status_code == 200:
                return response
            else:
                return None
        except Exception as e:
            if "Invalid URL" in str(e):
                return None

    def set_url(self):
        while True:
            self.clear_screen()
            input_url = input("Enter a URL: ")
            if self.is_valid_url(input_url):
                if input_url[-1] != "/":
                    input_url += "/"
                self.clear_screen()
                break
            else:
                continue
        return input_url

    def time_end(self):
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        spm = len(self.good_urls) / elapsed_time * 60
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        seconds = int(elapsed_time % 60)
        formatted_time = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
        formatted_spm = "{:.2f}".format(spm)
        print(f"Elapsed Time: {formatted_time}")
        print(f"Sites Found: {self.sites_looked}")
        print(f"Working Sites: {len(self.good_urls)}")
        print(f"Threads Used: {self.thread_counter}")
        print(f"Sites Per Minute: {formatted_spm}")
        
    def get_domain(self):
        domain = self.url
        domain = domain.strip("https://")
        domain = domain.strip("http://")
        domain = domain.split(".")
        del domain[0]
        domain = ".".join(domain)
        return domain

    def is_valid_url(self,input_url):
        parsed_url = urlparse(input_url)
        return all([parsed_url.scheme, parsed_url.netloc])

    def log(self):
        self.clear_screen()
        print("Ok Thats All I Got For Now\nYour Results Are Waiting For You In 'log.json' File\nGo Catch Them All!\nAnd Btw Here Some Stats If Youre Intrested :D")
        self.time_end()
        path = self.make_dir("Crawler")
        with open(f"{path}/log.json","w") as json_file:
            json_file.writelines(json.dumps(self.good_urls,indent=2))

    def menu(self):     
        while True:
            self.clear_screen()
            print("\n               Welcome To Website Crawler Module                 \n")
            print("*******************************************************************\n")
            print("|                                                                 |\n")
            print("|    Options:                                                     |\n")
            print("|    [1] Use Crawler Only                                         |\n")
            print("|    [2] Add Some BruteForce!! (In Progress...)                   |\n")
            print("|                                                                 |\n")
            print("*******************************************************************\n")
            choise = input()
            if choise in ["1"]:
                break
        while True:
            self.clear_screen()
            print("\n               Welcome To Website Crawler Module                 \n")
            print("*******************************************************************\n")
            print("|                                                                 |\n")
            print("|    Options:                                                     |\n")
            print("|    [1] Fast Crawl (only sites)                                  |\n")
            print("|    [2] Slow Crawl (sites and requests) - Recommended            |\n")
            print("|                                                                 |\n")
            print("*******************************************************************\n")
            choise = input()
            if choise == "1":
                self.scan_type = "?"
                break
            elif choise == "2":
                self.scan_type = "#"
                break   
        self.url = self.set_url()
        print(f"Crawling at: {self.url}\nTry to stay quiet")
    
    def make_dir(self,folder):
        try:
            cwd = os.getcwd()
            time = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
            path = f"{cwd}/Results/{folder}_Results/{time}"
            os.makedirs(path,exist_ok=True)
            return path
        except Exception:
            self.clear_screen()
            print("Error:\n")
            print("Creating Folders Failed!\n")
            print("Press Enter To Exit...\n")
            input()
            exit()

    def clear_screen(self):
        try:
            os.getuid()
            subprocess.run("clear",shell=True)
        except AttributeError:
            subprocess.run("cls",shell=True)

Crawler()
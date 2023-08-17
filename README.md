# Cyber Security Automation Project

Welcome to the Cyber Security Automation project! This repository contains a collection of modules designed to automate various cybersecurity tasks. The project aims to streamline and simplify the process of reconnaissance, scanning, and other security-related activities.

## Modules

### 1. Recon Module

The Recon Module focuses on information gathering and reconnaissance techniques.

- **WHOIS SCAN:** Perform WHOIS lookups to gather information about domain registrations and ownership.

- **DNS ENUMERATION:** Enumerate DNS records to gather information about the target's domain.

- **Subdomain Brute Force (BF):** Utilize subdomain brute force techniques to discover additional subdomains associated with the target.

- **Web Directories Brute Force (BF):** Perform brute force scans on web directories to identify hidden or sensitive directories.

### 2. Scanning Module

The Scanning Module involves various scanning techniques to assess network and system vulnerabilities.

- **ARP Scanner + Nmap Scan:** Combine ARP scanning and Nmap scanning to identify devices on the local network and perform detailed port scans.

- **ARP Scanner + Scan with Python Socket Library:** Employ ARP scanning along with Python Socket Library to assess network device presence and identify open ports.

### 3. Misc Tools

The Misc Tools section contains various utility tools for different security-related tasks.

- **ARP Scanner:** A tool for ARP scanning to discover devices on a local network.

- **Ping Sweeper:** A tool for performing ping sweeps to identify active hosts on a network.

- **Basic Port Scanner with Socket Library:** A simple port scanning tool using Python's socket library to check for open ports.

- **Kernel CVE Auto Scanner from CPE:** An automatic scanner that identifies known vulnerabilities in the kernel based on Common Platform Enumeration (CPE) identifiers.

## Getting Started

To use the modules in this project, follow these steps:

1. Clone this repository: `git clone https://github.com/arielkl9/Cyber-Framework-Python.git`

2. Navigate to the desired module's directory: `cd Cyber-Framework-Python`

3. install the requirements 'pip install requirements.txt'

4. Run the script: `python framework.py`

5. Follow the instructions provided by the script to perform the desired task.

# Acceptable use

This toolkit performs active reconnaissance and scanning (WHOIS, DNS
enumeration, subdomain and directory brute forcing, ARP/ping discovery, port
and service scanning, and CVE lookups).

Only run it against systems you **own** or have **explicit, written
authorisation** to test. Unauthorised scanning may be illegal in your
jurisdiction and is a violation of most networks' acceptable-use policies.

Several features (ARP discovery, ping sweep) require raw-socket privileges and
therefore root/Administrator, and the Nmap scan requires `nmap` to be
installed and on `PATH`.

## Reporting a vulnerability

If you find a security issue in this project itself, please open a private
report via GitHub's security advisories rather than a public issue.

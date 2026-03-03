# What Is ReconSuite

ReconSuite is a personal project of me building offensive cybersecurity tools while practicing my coding skills, the tools that you will see here are designed for initial reconniassance.

Most of the tools here will not be perfect as I am constantly improving my skills. But feel free to download and use them on your targets (with explicit permission) and suggest features if you will be using them.

## List of Tools

**whois.py** - Simple tool that connects to iana's whois protocol (port 43) and extracts the records for the domain. theres an extra feature to recurse and find extra whois portals that will give a better result.

```
usage: whois.py [-h] [-i IP] [-n] [-s SERVER]

Whois lookup tool, enter an IP address and get its whois records

options:
  -h, --help           show this help message and exit
  -i, --ip IP          Enter domain address (example: google.com)
  -n, --no-recurse     Disable recursive WHOIS search
  -s, --server SERVER  WHOIS server to look at (example: whois.iana.org)
```

**extractor.py** - Simple tool to extract the most common word of a web page


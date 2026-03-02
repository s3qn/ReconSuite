### GOALS of project
"""
DONE 1. Get Whois IANA records.
DONE 2. Extract Referall from whois IANA record
DONE 3. Send them back to the referall site. Get the response and send it back
DONE 4. if there are extra referall whois sites, loop the sending to the site until we get the final optimized records idk if its the goal

THEY HAVE A DB 5. Find how some websites view old whois records. and create a strategy to implement into the current code
6. Think how to implement all information found in records and organize it nicely in an output

BUGS:
FIXED 1. Fix Registrar hosts like http://something to not mess with the extract function

"""

import socket
import argparse

def send_query(query, platform):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((platform, 43))
        s.send((query + "\r\n").encode())

    except socket.error:
        print("Error: IP could not be reached")
        exit(0)
    response = s.recv(4096).decode()
    s.close()
    return response


def extract_refer_link(response):
    response_split = response.splitlines()
    for line in response_split:
        stripped_line = line.strip()
        if stripped_line.startswith("refer:") or stripped_line.startswith("Registrar WHOIS Server:"):
            split_line = stripped_line.split(":", 1)
            extracted_link = split_line[1].strip()
            if extracted_link.startswith("http://"):
                return extracted_link.lstrip('http://')
            else:
                return extracted_link

    else:
        return "ERROR: Couldn't find refer link"

def recurse_link(query, response):
    refer_link = extract_refer_link(response)
    current_link = None

    while current_link != refer_link:
        if refer_link == "ERROR: Couldn't find refer link":
            if current_link is not None:
                print("Stopped searching at: " + current_link)
                break
            else:
                break
        current_link = refer_link
        print(f"Found whois refer: {refer_link}, Resending WHOIS request...")
        response = send_query(query, refer_link)
        refer_link = extract_refer_link(response)

    return response

def main():

    # Parse Arguments
    ap = argparse.ArgumentParser(description="Whois lookup tool, enter an IP address and get its whois records")
    ap.add_argument("-i", "--ip", required=False, help="Enter domain address (example: google.com)", default="facebook.com")
    ap.add_argument("-n", "--no-recurse", required=False, action='store_false', help="Disable recursive WHOIS search", dest="recurse")
    ap.add_argument("-s", "--server", required=False, help="WHOIS server to look at (example: whois.iana.org", default="whois.iana.org")
    args = ap.parse_args()

    print("Searching WHOIS records for: " + args.ip)
    print(f"Searching for domain on server: {args.server}")
    response = send_query(args.ip, args.server)

    if args.recurse:
        response = recurse_link(args.ip, response)

    print("------ Results ------")
    print(response)

if __name__ == "__main__":
    main()




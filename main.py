import digitalocean
import requests
import subprocess
import shlex
import time

from dotenv import dotenv_values
config = dotenv_values('.env')

TOKEN = config['DIGITALOCEAN_ACCESS_TOKEN']
DOMAIN = config['DOMAIN']
#empty list to cast to int
ID_LIST = []
#looping over config to grab str ids
lst = config['ID_LIST'].split(" ")
for i in lst:
    ID_LIST.append(int(i))


def timeit(function):
    '''generalized time function'''
    t0 = time.time()
    function()
    t1=time.time()
    return(t1-t0)

def testing(domain=DOMAIN, id_list=ID_LIST, token=TOKEN):
    conn = digitalocean.Domain(token=TOKEN, name=DOMAIN)
    records = conn.get_records()
    for r in records:
        print(r.name, r.domain, r.type, r.data, r.id)


def printit():
    return("local ip {} and dns dig {}".format(getip(), dig()))


def getip():
    '''function to check the ip address of current local computer'''
    return(requests.get("http://www.myexternalip.com/raw").text)


def dig(domain=DOMAIN):
    '''function to check the ip address of domain provided'''
    #setting cmd to pass to bash, dig + domain +short to only get ip
    cmd = 'dig {} +short'.format(domain)
    #passing to subprocess, piping output to proc
    proc=subprocess.Popen(shlex.split(cmd),stdout=subprocess.PIPE)
    #getting output and error from commincation
    out,err=proc.communicate()
    #catching errors and handling them poorly
    try:
        return(out.decode('utf-8').strip("\n"))
    except NameError:
        return(err.decode('utf-8'))



def update(domain=DOMAIN, id_list=ID_LIST, token=TOKEN):
    '''update digital ocean domain form id list'''
    #create connection
    connection = digitalocean.Domain(token=token, name=domain)
    #get records
    records = connection.get_records()
    #id is passed to return at the end, sets to true if its updated, otherwise its false, so you can check if its passed successfully
    id = None
    #loop thru records
    for r in records:
        #if the dns entry id number matches a  number in the id list, it will udpate it with the getip() funciton
        if r.id in id_list:
            r.data = getip()
            r.save()
            id = True
        elif r is records[-1]:
            #prints nothing
            id = False
    #return true to handle logic
    return(id)


def check(domain=DOMAIN, id_list=ID_LIST, token=TOKEN):
    '''function to check local and dns ip address'''
    if getip() == dig():
        return(True)
    else:
        return(False)

def main(domain=DOMAIN, id_list=ID_LIST, token=TOKEN):
    '''main function to call on script, to execute all scripts in order'''
    compare = check()
    if compare == True:
        #check weather ips match, if true, print they match
        print("local and {} ip match".format(domain))
    else:
        #if ips dont match, push update to digitalocean
        pushupdate = update()
        if pushupdate == True:
            #cathcing weather there was a problem
            print("no update made to {} domain".format(domain))
        elif pushupdate == False:
            #here we go
            print("updated {} to new address".format(domain))


if __name__ == "__main__":
    main()

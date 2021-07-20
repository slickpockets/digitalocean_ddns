import digitalocean
import requests
import subprocess
import shlex
import time

from dotenv import dotenv_values
config = dotenv_values('.env')

TOKEN = config['DIGITALOCEAN_ACCESS_TOKEN']
DOMAIN = config['DOMAIN']
ID_LIST = config['ID_LIST'].split(" ")


def timeit(function):
    '''generalized time function'''
    t0 = time.time()
    function()
    t1=time.time()
    return(t1-t0)

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
    connection =    digitalocean.Domain(token=token, name=domain)
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


def main(domain=DOMAIN, id_list=ID_LIST, token=TOKEN):
    check = update()
    if check == False:
        return("local and {} ip match".format(domain))
    elif check == True:
        return("updated {} to new address".format(domain))


if __name__ == "__main__":
    main()

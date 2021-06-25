import digitalocean
import requests
import os

for line in open('.env'):
    var = line.strip().split('=')
    if len(var) == 2:
        os.environ[var[0]] = var[1]

token = os.environ['DIGITALOCEAN_ACCESS_TOKEN']
domain_name = os.environ['DOMAIN']
id_list = os.environ['ID_LIST'].split(" ")

def getip():
    return(requests.get("http://www.myexternalip.com/raw").text)

def updateip(ip_new, domain_name, token):
    domain = digitalocean.Domain(token=token, name=domain_name)
    records = domain.get_records()
    id = None
    for r in records:
        if r.id in id_list:
            r.data = ip_new
            r.save()

def filewrite(file='ip.txt', data=''):
    with open(file, 'w') as f:
        f.write(data)
        f.close()

def fileread(file='ip.txt'):
    ip = None
    try:
        with open(file, 'r') as f:
            ip = f.readline()
            f.close()
            return(ip)
    except FileNotFoundError:
        print('ip file doesnt exist, creating it')
        ip='doesnt matter'
        filewrite(file, data=ip)
        return(ip)



def checkip(ip_old=fileread().strip('\n'), ip_new=getip(), domain_name=domain_name, token=token):
    if str(ip_old) == str(ip_new):
        return("same")
    else:
        print('ip changed, updating ip {} to {} for {}'.format(ip_old, ip_new, domain_name))
        updateip(ip_new, domain_name, token)
        print('updated digital ocean, writing data to file')
        filewrite(file='ip.txt', data=ip_new)
        return("updated")

if __name__ == "__main__":
    checkip(ip_old=fileread().strip('\n'), ip_new=getip(), domain_name=domain_name, token=token)

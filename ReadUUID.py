import json
import subprocess
import sys
import socket

def DefineIp():
    try:
        #Define workers ip address.
        with open('IpAddress.json', 'r') as f:
            JsonData = json.loads(f.read())
        Worker1_IP = JsonData['worker1']
        Worker2_IP = JsonData['worker2']
        Worker3_IP = JsonData['worker3']
        return Worker1_IP, Worker2_IP, Worker3_IP
    except:
        return "IP error."

def run():
    #data[1]:pmem block uuid
    data = sys.argv
    try:
        with open('./uuidFile/'+ data[1] +'.json', 'r') as myfile:
            data=myfile.read()
        obj = json.loads(data)
        print(obj)
    except OSError as e:
        #Define workers ip address.
        Worker1_IP, Worker2_IP, Worker3_IP = DefineIp()
        IP = get_host_ip()
        if str(IP) == Worker1_IP:
            print("Worker1. Find Fail.")
        elif str(IP) == Worker2_IP:
            print("Worker2. Find Fail.")
        else:
            print("Worker3. Find Fail.")

#Use get_host_ip function to get local ip
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

run()

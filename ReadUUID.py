import json
import subprocess
import sys
import socket


def run():
    data = sys.argv
    try:
        with open('./uuidFile/'+ data[1] +'.json', 'r') as myfile:
            data=myfile.read()
        obj = json.loads(data)
        print(obj)
    except OSError as e:
        Worker1_IP = '140.92.152.88'
        Worker2_IP = '140.92.152.72'
        Worker3_IP = '140.92.152.63'

        IP = get_host_ip()
        if str(IP) == Worker1_IP:
            print("Worker1. Find Fail.")
        elif str(IP) == Worker2_IP:
            print("Worker2. Find Fail.")
        else:
            print("Worker3. Find Fail.")

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


run()

import requests
import subprocess
import sys
import json
import os.path
from os import path

Worker1_IP = ''
Worker2_IP = ''
Worker3_IP = ''

while(1):
    """this while loop can classification 5 mode.
    Arge:
        mode_chose(int): The mode to use
    
    Return:
        string(str): Return different mode's information.
    """
    print("Please enter your required items:\n","0.Create and mount memery.; 1.Delete umount memery.; 2.Show Block Device.; 3.Exit.")
    mode_chose = input("Item selection:")

    if str(mode_chose)==str("0"):
        #The folder name which you want to mount on the namespace
        folder_name = input("folder name:")
        #The pmem blocks size you want to create
        create_size = input("create size:")
        
        #try to post json to Worker1 /create api
        try:
            worker = requests.post(Worker1_IP + '/create', json={"folder_name":folder_name,"create_size":create_size})
            if worker.ok:
                if str(worker.text)=="Worker1: Your required capacity is too large!(Or the format is incorrect)":
                    pass
                else:
                    print(worker.text+"\n")
                    continue
        except requests.ConnectionError:
            pass

        #try to post json to Worker2 /create api
        try:
            worker = requests.post(Worker2_IP + '/create', json={"folder_name":folder_name,"create_size":create_size})
            if worker.ok:
                if str(worker.text)=="Worker2: Your required capacity is too large!(Or the format is incorrect)":
                    pass
                else:
                    print(worker.text+"\n")
                    continue
        except requests.ConnectionError:
            pass

        #try to post json to Worker3 /create api
        try:
            worker = requests.post(Worker3_IP + '/create', json={"folder_name":folder_name,"create_size":create_size})
            if worker.ok:
                if str(worker.text)=="Worker3: Your required capacity is too large!(Or the format is incorrect)":
                    pass
                else:
                    print(worker.text+"\n")
                    continue
        except requests.ConnectionError:
            pass

        print("Your required capacity is too large!(Or the format is incorrect)\n")

    if str(mode_chose)==str("1"):
        #The peme blocks uuid you want to delete
        Delete_SpaceName = input("The name of the region you need to delete:")

        #try to post json to Worker1 /DeleteUUID api
        try:
            Worker1_delete = requests.post(Worker1_IP + '/DeleteUUID', json={"UUID":Delete_SpaceName})
            CallDeleteFun = Worker1_delete.text
            if str(CallDeleteFun)=="Worker1. Delete Success.":
                print("Work1. Delete Success.\n")
                continue
        except requests.ConnectionError:
            pass

        #try to post json to Worker2 /DeleteUUID api
        try:
            Worker2_delete = requests.post(Worker2_IP + '/DeleteUUID', json={"UUID":Delete_SpaceName})
            CallDeleteFun = Worker2_delete.text
            if str(CallDeleteFun)=="Worker2. Delete Success.":
                print("Work2. Delete Success.\n")
                continue
        except requests.ConnectionError:
            pass

        #try to post json to Worker3 /DeleteUUID api
        try:
            Worker3_delete = requests.post(Worker3_IP + '/DeleteUUID', json={"UUID":Delete_SpaceName})
            CallDeleteFun = Worker3_delete.text
            if str(CallDeleteFun)=="Worker3. Delete Success.":
                print("Work3. Delete Success.\n")
                continue
        except requests.ConnectionError:
            pass

        print("Workers UUID don't exist.\n")

    if str(mode_chose)==str("2"):
        ModeTwoChose = input("Please enter your required items: 1.pmem list availcapacity.; 2.pmem list blkdev.\nItem selection:")
        if ModeTwoChose=="1":
            WorkerOneAvailcapacity = requests.post(Worker1_IP + '/availcapacity')
            WorkerTwoAvailcapacity = requests.post(Worker2_IP + '/availcapacity')
            WorkerThreeAvailcapacity = requests.post(Worker3_IP + '/availcapacity')
            
            if WorkerOneAvailcapacity=="":
                print("None.")
            else:
                print("Worker1:\n"+WorkerOneAvailcapacity.text)
            print("\n")
            
            if WorkerTwoAvailcapacity=="":
                print("None.")
            else:
                print("Worker2:\n"+WorkerTwoAvailcapacity.text)
            print("\n")
            
            if WorkerThreeAvailcapacity=="":
                print("None.")
            else:
                print("Worker3:\n"+WorkerThreeAvailcapacity.text)
            print("\n")
            
        elif ModeTwoChose=="2":
            WorkerOneBlkdev = requests.post(Worker1_IP + '/blkdev')
            WorkerTwoBlkdev = requests.post(Worker2_IP + '/blkdev')
            WorkerThreeBlkdev = requests.post(Worker3_IP + '/blkdev')
            
            if WorkerOneBlkdev.text=="":
                print("Worker1: None.\n")
            else:
                print("Worker1:\n"+WorkerOneBlkdev.text+"\n")
            print("\n")
            
            if WorkerTwoBlkdev.text=="":
                print("Worker2 None.\n")
            else:
                print("Worker2:\n"+WorkerTwoBlkdev.text+"\n")
            print("\n")
            
            if WorkerThreeBlkdev.text=="":
                print("Worker3 None.\n")
            else:
                print("Worker3:\n"+WorkerThreeBlkdev.text+"\n")
            print("\n")
            
        else:
            print("wrong format.\n")


    if str(mode_chose)==str("3"):
        print("Exit!"+"\n")
        exit(0)

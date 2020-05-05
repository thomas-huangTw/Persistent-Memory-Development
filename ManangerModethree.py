import requests
import subprocess
import sys
import json
import os.path
from os import path

Worker1_IP = 'http://140.92.152.88:1234'
Worker2_IP = 'http://140.92.152.72:1234'
Worker3_IP = 'http://140.92.152.63:1234'

Count=1
while Count!=int(0):
    print("Please enter your required items:\n","0.Create and mount memery.; 1.Delete umount memery.; 2.Show Block Device.; 3.Exit.")
    mode_chose = input("Item selection:")

    if str(mode_chose)==str("0"):
        folder_name = input("folder name:")
        create_size = input("create size:")
        worker1 = requests.post(Worker1_IP + '/create', json={"folder_name":folder_name,"create_size":create_size})
        if worker1.ok:
            if str(worker1.text)=="Worker1: Your required capacity is too large!(Or the format is incorrect)":
                worker3 = requests.post(Worker3_IP + '/create', json={"folder_name":folder_name,"create_size":create_size})
                if worker3.ok:
                    print(worker3.text+"\n")
                else:
                    print(worker1.text+"\n")

    if str(mode_chose)==str("1"):
        Delete_SpaceName = input("The name of the region you need to delete:")
        Worker1_delete = requests.post(Worker1_IP + '/DeleteUUID', json={"UUID":Delete_SpaceName})
        CallDeleteFun = Worker1_delete.text
        if str(CallDeleteFun)=="Worker1. Delete Success.":
            print("Work1. Delete Success.\n")
        elif str(CallDeleteFun)=="Worker1. No this UUID." and (requests.post(Worker3_IP + '/FindUUID', json={"UUID":Delete_SpaceName})).text!="Worker3. Find Fail.\n":
            DeleteWorker2UUID = requests.post(Worker3_IP + '/DeleteUUID', json={"UUID":Delete_SpaceName})
            print(DeleteWorker2UUID.text+"\n")
        else:
            print("Workers UUID don't exist.\n")

    if str(mode_chose)==str("2"):
        ModeTwoChose = input("Please enter your required items: 1.pmem list availcapacity.; 2.pmem list blkdev.\nItem selection:")
        if ModeTwoChose=="1":
            WorkerOneAvailcapacity = requests.post(Worker1_IP + '/availcapacity')
            WorkerTwoAvailcapacity = requests.post(Worker3_IP + '/availcapacity')
            if WorkerOneAvailcapacity=="":
                print("None.")
            else:
                print("Worker1:\n"+WorkerOneAvailcapacity.text)
            print("\n")
            if WorkerTwoAvailcapacity=="":
                print("None.")
            else:
                print("Worker3:\n"+WorkerTwoAvailcapacity.text)
        elif ModeTwoChose=="2":
            WorkerOneBlkdev = requests.post(Worker1_IP + '/blkdev')
            WorkerTwoBlkdev = requests.post(Worker3_IP + '/blkdev')
            if WorkerOneBlkdev.text=="":
                print("Worker1: None.\n")
            else:
                print("Worker1:\n"+WorkerOneBlkdev.text+"\n")
            print("\n")
            if WorkerTwoBlkdev.text=="":
                print("Worker3 None.\n")
            else:
                print("Worker3:\n"+WorkerTwoBlkdev.text+"\n")
        else:
            print("Not yet.\n")
    if str(mode_chose)==str("3"):
        print("Exit!"+"\n")
        Count = 0

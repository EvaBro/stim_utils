# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:42:40 2026

@author: Eva Broeders with help from Claude AI, based on the matlab script in 
C:/Users/MEG Stim/Documents/OptiTrack

"""

import ctypes
import sys
import time
from datetime import datetime
import psutil

sys.path.append(r'C:\Users\MEG Stim\Documents\OptiTrack\Matlab_files\NatNet_SDK_3.1\NatNetSDK\Samples\PythonClient')
from NatNetClient import NatNetClient

io = ctypes.WinDLL("inpoutx64.dll")
address = 53240

def is_motive_running():
    """Check if Motive.exe is running."""
    return any(p.name().lower() == "motive.exe" for p in psutil.process_iter(['name']))

def send_trigger(value):
    io.Out32(address, value)

def setup():
    if not is_motive_running():
        print("Motive is not running. Optitrack will be disabled.")
        response = input("Continue without Optitrack? (y/n): ").strip().lower()
        if response == 'y':
            return None
        else:
            sys.exit("Experiment aborted: Motive is not running.")
    send_trigger(0)
    client = NatNetClient()
    client.serverIPAddress = "127.0.0.1"
    client.localIPAddress  = "127.0.0.1"
    # Manually open only the command socket, we don't need to read data via a separate thread:
    client.commandSocket = client._NatNetClient__createCommandSocket()
    return client

def start_recording(client):
    #input("Press Enter to start recording...")
    print('Started Optitrack recording')
    send_trigger(2)
    client.sendCommand(NatNetClient.NAT_REQUEST, "StartRecording",
        client.commandSocket, (client.serverIPAddress, client.commandPort))
    time.sleep(0.05)
    send_trigger(0)
    
def stop_recording(client):
    client.sendCommand(NatNetClient.NAT_REQUEST, "StopRecording",
        client.commandSocket, (client.serverIPAddress, client.commandPort))
    print('Stopped Optitrack recording')
    
def set_take_name(client, takename):
    now=datetime.now()
    client.sendCommand(NatNetClient.NAT_REQUEST, "SetRecordTakeName,"+takename+' ' +now.strftime("%Y-%m-%d %H_%M_%S"),
        client.commandSocket, (client.serverIPAddress, client.commandPort))
    print('Optitrack take name: ' +takename+' ' +now.strftime("%Y-%m-%d %H_%M_%S"))
    time.sleep(0.1) # Optitrack needs some time to fully register the take name and set it as the current take
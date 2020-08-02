

"""https://api.meraki.com/api/v0/networks/N_711005791171205780/cameras/Q2JV-BY67-ABC8/snapshot'

network : N_711005791171205780
"""

import os
import configparser
import sys
import json
import requests
from redisai import Client
# import boto3
import paho.mqtt.client as mqtt
from PIL import Image
import requests
from io import BytesIO
import datetime
import pytz
import logging
import time

session = requests.Session()

res_arr = []

BASE_PATH = os.path.join(os.getcwd(), "credentials.ini")

(API_KEY, NET_ID, MV_SERIAL, SERVER_IP) = gather_credentials(BASE_PATH)

def iso(ts):
    # return time.strftime("%Y %d %b %H:%M:%S +0000", time.localtime(ts))
    d = datetime.datetime.utcfromtimestamp(ts/1000).isoformat()
    return d[:-7]+'Z'

def url_to_img(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def on_connect(mq_client, userdata, flags, result_code):
    """The callback for when the client receives a CONNACK response from the server"""
    print(f'Connected with result code {result_code}')
    serial = userdata['MV_SERIAL']
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    mq_client.subscribe(f'/merakimv/{serial}/raw_detections')
    #client.subscribe(f'/merakimv/{serial}/light')


def on_message(client, userdata, msg):
    """When a PUBLISH message is received from the server, get a
    URL to analyse"""
    #triggers image analysis when incoming MQTT data is detected
    # print(client, userdata, msq)
    # client.loop(.1)
    time.sleep(0.01)
    obj = msg.payload.decode("utf-8")
    res = json.loads(obj)
    print(res)
    objs = res['objects']
    person_count = len(objs)
    ts = res['ts']
    # print(ts, person_count)
    if(person_count>0):
        ts = iso(ts)
        # s_url = get_meraki_snapshots(API_KEY, NET_ID, ts)
        # res['url'] = s_url
        res_arr.append(ts)
        print("Item Saved with person > 0 and timestamp: ", ts)

# def analyze(ts):
#     """periodially takes snap URL from Meraki, sends to AWS rekognition"""
#     flag = True
#     if flag:
#         # print("Request Snapshot URL")
#         #get the URL of a snapshot from our camera
#         ts_arr.append(ts)

def get_meraki_snapshots(session, api_key, net_id, time=None):
    """Get devices of network"""
    headers = {
        'X-Cisco-Meraki-API-Key': api_key,
        'Content-Type': 'application/json'
        # issue where this is only needed if timestamp specified
    }
    response = session.get(f'https://api.meraki.com/api/v0/networks/{net_id}/devices',
                           headers=headers)
    devices = response.json()
    #filter for MV cameras:
    cameras = [device for device in devices if device['model'][:2] == 'MV']
    # Assemble return data
    for camera in cameras:
        #filter for serial number provided
        if camera["serial"] == MV_SERIAL:
            # Get snapshot link
            if time:
                headers['Content-Type'] = 'application/json'
                response = session.post(
                    f'https://api.meraki.com/api/v0/networks/{net_id}/cameras/{camera["serial"]}/snapshot',
                    headers=headers,
                    data=json.dumps({'timestamp': time}))
            else:
                response = session.post(
                    f'https://api.meraki.com/api/v0/networks/{net_id}/cameras/{camera["serial"]}/snapshot',
                    headers=headers)

            # Possibly no snapshot if camera offline, photo not retrievable, etc.
            print(response.json())
            if response.ok:
                snapshot_url = response.json()['url']
                return snapshot_url
            else:
                return None
        else:
            return None

def gather_credentials(BASE_PATH):
    """Gather Meraki credentials"""
    conf_par = configparser.ConfigParser()
    try:
        conf_par.read(os.path.join(BASE_PATH, 'credentials.ini'))
        # conf_par.read('credentials.ini')
        cam_key = conf_par.get('meraki', 'key')
        net_id = conf_par.get('meraki', 'network')
        mv_serial = conf_par.get('sense', 'serial')
        server_ip = conf_par.get('server', 'ip')
    except:
        print('Missing credentials or input file!')
        sys.exit(2)
    return cam_key, net_id, mv_serial, server_ip

def print_urls(session, res_arr):#, API_KEY, NET_ID):
    url_arr = []
    for ts in res_arr:
        s_url = get_meraki_snapshots(session, API_KEY, NET_ID, ts)
        url_arr.append(s_url)

def disconnect(client):
    logging.debug("Disconnected")
    client.loop_stop()

def connect_camera():
    
    USER_DATA = {
        'API_KEY': API_KEY,
        'NET_ID': NET_ID,
        'MV_SERIAL': MV_SERIAL,
        'SERVER_IP': SERVER_IP
    }
    # Start MQTT client
    client = mqtt.Client()
    client.user_data_set(USER_DATA)
    #on connection to a MQTT broker:
    client.on_connect = on_connect
    #when an MQTT message is received:
    client.on_message = on_message
    #specify the MQTT broker here
    client.connect(SERVER_IP, 1883, 300)
    client.loop_start()

if __name__ == '__main__':
    
    # (API_KEY, NET_ID, MV_SERIAL, SERVER_IP) = gather_credentials(BASE_PATH)
    connect_camera()

    print(res_arr)

# iso(1596282058612)
#2020-08-01T11:40:58Z

# !curl -L -H 'X-Cisco-Meraki-API-Key: e4edb0ff642754d2b1f7146967edb38b34b3e49c' -X POST 'https://api.meraki.com/api/v0/networks/N_711005791171205780/cameras/Q2JV-BY67-ABC8/snapshot'


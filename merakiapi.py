import configparser
import sys
import json
import requests
import boto3
import paho.mqtt.client as mqtt
from PIL import Image
import requests
from io import BytesIO

def url_to_img(url):
  response = requests.get(url)
  img = Image.open(BytesIO(response.content))
  return img

ts_arr = []

def on_connect(mq_client, userdata, flags, result_code):
    """The callback for when the client receives a CONNACK response from the server"""
    print(f'Connected with result code {result_code}')
    serial = userdata['MV_SERIAL']
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    mq_client.subscribe(f'/merakimv/{serial}/0')
    #client.subscribe(f'/merakimv/{serial}/light')

def on_message(client, userdata, msg):
    """When a PUBLISH message is received from the server, get a
    URL to analyse"""
    #triggers image analysis when incoming MQTT data is detected
    # print(client, userdata, msq)
    obj = msg.payload.decode("utf-8")
    obj = json.loads(obj)
    person_count = obj['counts']['person']
    ts = obj['ts']
    print(ts, person_count)
    if(person_count>=0):
      # print("message rex", obj)
      analyze(ts)

def analyze(ts):
    """periodially takes snap URL from Meraki, sends to AWS rekognition"""
    flag = True
    if flag:
        # print("Request Snapshot URL")
        #get the URL of a snapshot from our camera
        
        ts_arr.append(ts)
        

def get_meraki_snapshots(api_key, net_id, time=None):
    """Get devices of network"""
    headers = {
        'X-Cisco-Meraki-API-Key': api_key,
        # 'Content-Type': 'application/json'
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

def gather_credentials():
    """Gather Meraki credentials"""
    conf_par = configparser.ConfigParser()
    try:
        conf_par.read(os.path.join(BASE_PATH, 'credentials.ini'))
        cam_key = conf_par.get('meraki', 'key')
        net_id = conf_par.get('meraki', 'network')
        mv_serial = conf_par.get('sense', 'serial')
        server_ip = conf_par.get('server', 'ip')
    except:
        print('Missing credentials or input file!')
        sys.exit(2)
    return cam_key, net_id, mv_serial, server_ip

if __name__ == '__main__':

    (API_KEY, NET_ID, MV_SERIAL, SERVER_IP) = gather_credentials()
    USER_DATA = {
        'API_KEY': API_KEY,
        'NET_ID': NET_ID,
        'MV_SERIAL': MV_SERIAL,
        'SERVER_IP': SERVER_IP
    }
    session = requests.Session()
    # Start MQTT client
    client = mqtt.Client()
    client.user_data_set(USER_DATA)
    #on connection to a MQTT broker:
    client.on_connect = on_connect
    #when an MQTT message is received:
    client.on_message = on_message
    #specify the MQTT broker here
    client.connect(SERVER_IP, 1883, 300)
    client.loop_forever()

img_arr = []
for ts in ts_arr:
  print(ts)
  s_url = get_meraki_snapshots(API_KEY, NET_ID, iso(ts))
  img_arr.append(s_url)
  

# !curl -L -H 'X-Cisco-Meraki-API-Key: e4edb0ff642754d2b1f7146967edb38b34b3e49c' -X POST 'https://api.meraki.com/api/v0/networks/N_711005791171205780/cameras/Q2JV-BY67-ABC8/snapshot'

s_url = get_meraki_snapshots(API_KEY, NET_ID, iso(ts_arr[4]))

import datetime
import pytz
# from datetime import datetime
import time

def iso(ts):
  return time.strftime("%Y%d %b  %H:%M:%S +0000", time.localtime(ts))
  # return datetime.datetime.utcfromtimestamp(ts/1000).isoformat()
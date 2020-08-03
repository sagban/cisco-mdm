"""https://api.meraki.com/api/v0/networks/N_711005791171205780/cameras/Q2JV-BY67-ABC8/snapshot'

network : N_711005791171205780
"""

import os
import configparser
import sys
import json
import paho.mqtt.client as mqtt
from PIL import Image
import requests
from io import BytesIO
import datetime
import logging
import time
from ..redis_connection import connection
from json import JSONEncoder, JSONDecoder
session = requests.Session()

API_KEY = "e4edb0ff642754d2b1f7146967edb38b34b3e49c"
NET_ID = "N_711005791171205780"
MV_SERIAL = "Q2JV-BY67-ABC8"
SERVER_IP ="52.10.7.74"
USER_DATA = {
      'API_KEY': "e4edb0ff642754d2b1f7146967edb38b34b3e49c",
      'NET_ID': "N_711005791171205780",
      'MV_SERIAL': "Q2JV-BY67-ABC8",
      'SERVER_IP': "52.10.7.74"
  }
res_arr = []
urls_arr = []
MAX_IMAGES = 50
global con
global oids
oids = {}
con = False
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


def redis_conn(con = False):
  con = connection._checkconnection(con)
  if not con:
    con = connection._connect()
  return con

con = redis_conn()

def iso(ts):
    # return time.strftime("%Y %d %b %H:%M:%S +0000", time.localtime(ts))
    d = datetime.datetime.utcfromtimestamp(ts/1000).isoformat()
    return d[:-7]+'Z'

def url_to_img(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img




def add_image_to_stream():
    stream = con.execute_command('xread', 'block', 50000, 'streams', 'urls', '$')
    # url = stream[b'url']
    url = "some dummy"
    image = url_to_img(url)
    try:
        # con.execute_command('xadd', 'images', '*', 'img', image)
        con.xadd("images", {"img": image})
        print("Image added to stream!")
    except:
        print("Check again")

def get_images_from_stream():
    # stream = con.execute_command('xread', 'block', 50000, 'streams', 'images:0', '$')
    # return stream[b'img]
    return con.xread({'images': b'0-0'})




#Gather URLs and store to the redis streams
def gather_urls(session, ts):#, API_KEY, NET_ID):
    url_arr = []
    encoder = JSONEncoder()
    # try:
    s_url = get_meraki_snapshots(session, API_KEY, NET_ID, ts)
    url_arr.append(s_url)
    # con.xadd('urls', {"url": encoder.encode(s_url)})
    print(s_url)
    # x = con.execute_command('xadd', 'urls', 'MAXLEN', '~', str(MAX_IMAGES), '*', 'url', encoder.encode(s_url) , 'ts', encoder.encode(ts))
    print("Added: URL")
    return s_url
    # except:
    #     print("Not Saved: URL")
    # return


def read_person_stream():
  x = con.execute_command('xread', 'block', '5000', 'streams', 'person', '$')
  decoder = JSONDecoder()
  print(decoder.decode(x))

  read_person_stream()

def add_person_stream(person):
  encoder = JSONEncoder()
  try:
    x = con.execute_command('xadd','person', 'MAXLEN', '~', str(MAX_IMAGES), '*', 'person', encoder.encode(person))

    # gather_urls(session, person['ts'])
    print("Added: Person Object")
  except:
    print("Not Saved: Person Object")
  return


def on_connect(mq_client, userdata, flags, result_code):
    """The callback for when the client receives a CONNACK response from the server"""
    print(f'Connected with result code {result_code}')
    serial = userdata['MV_SERIAL']
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # time.sleep(2)
    mq_client.subscribe(f'/merakimv/{serial}/raw_detections')
    #client.subscribe(f'/merakimv/{serial}/light')


def on_message(client, userdata, msg):
    """When a PUBLISH message is received from the server, get a
    URL to analyse"""
    #triggers image analysis when incoming MQTT data is detected
    # print(client, userdata, msq)
    # client.loop(.1)
    obj = msg.payload.decode("utf-8")
    res = json.loads(obj)
    # print(res)
    objs = res['objects']

    for head in objs:
      if head['type'] == 'person':
        oids[head['oid']] = True

    person_count = len(oids.keys())
    ts = res['ts']
    print(ts, person_count)
    if int(person_count) > 0:
        ts = iso(ts)
        # s_url = get_meraki_snapshots(API_KEY, NET_ID, ts)
        # res['url'] = s_url
        person = res
        person['ts'] = ts
        person['person_count'] = person_count
        # person['s_url'] = s_url
        # print("Item Saved with person > 0 and timestamp: ", person)
        # add_person_stream(person)
        res_arr.append(person)
        print(person)
        # print("Item Saved with person > 0 and timestamp: ", ts)

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
    print("Hi from snap")
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



def print_urls(session, res_arr):#, API_KEY, NET_ID):
    url_arr = []
    for ts in res_arr:
        time.sleep(5)
        s_url = get_meraki_snapshots(session, API_KEY, NET_ID, ts)
        url_arr.append(s_url)


#stopping the flow
def disconnect():
  logging.debug("Disconnected")
  client.loop_stop()
  return res_arr


#connect to the camera and start the process
def connect_camera():
  # BASE_PATH = "credentials.ini"
  # (API_KEY, NET_ID, MV_SERIAL, SERVER_IP) = gather_credentials(BASE_PATH)
  # Start MQTT client
  res_arr.clear()
  urls_arr.clear()
  oids.clear()
  global client
  client = mqtt.Client()
  client.user_data_set(USER_DATA)
  #on connection to a MQTT broker:
  client.on_connect = on_connect
  #when an MQTT message is received:
  client.on_message = on_message
  #specify the MQTT broker here
  client.connect(USER_DATA['SERVER_IP'], 1883, 300)
  client.loop_start()
  # read_person_stream()
  return


#return all the snapshot urls
def get_urls():
  if len(urls_arr) > 0:
    return urls_arr
  else:
    for res in res_arr:
      ts = res['ts']
      urls_arr.append(gather_urls(session, ts))
    return urls_arr

if __name__ == '__main__':

    # (API_KEY, NET_ID, MV_SERIAL, SERVER_IP) = gather_credentials(BASE_PATH)
    (API_KEY, NET_ID, MV_SERIAL, SERVER_IP) = gather_credentials(BASE_PATH)
    # connect_camera()

    print(res_arr)

# iso(1596282058612)
#2020-08-01T11:40:58Z

# !curl -L -H 'X-Cisco-Meraki-API-Key: e4edb0ff642754d2b1f7146967edb38b34b3e49c' -X POST 'https://api.meraki.com/api/v0/networks/N_711005791171205780/cameras/Q2JV-BY67-ABC8/snapshot'


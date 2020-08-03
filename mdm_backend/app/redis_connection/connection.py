import redis
from urllib.parse import urlparse

global con

def _connect():
  global con
  url = urlparse("redis://127.0.0.1:6379")
  con = redis.Redis(host=url.hostname, port=url.port)
  return _checkconnection(con)

def _checkconnection(con):
  if not con:
    print("Not Connected!")
    return False
  print("Connected!")
  return con

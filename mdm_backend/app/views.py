import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .meraki_api import meraki_api
from .face_recognition import api, face_recognition

# Create your views here.

message = ["FAILURE", "SUCCESS", 'NOT_FOUND']

def format_response(data):
  return HttpResponse(
      serializers.serialize("json", data),
      content_type="text/json-comment-filtered"
  )

def res(status, message, data = None):
  args = {
    "status": status,
    "message": message,
    "data": data
  }
  return json.dumps(args)


@csrf_exempt
@api_view(['GET'])
def home(request):

  if request.method == 'GET':
    args = {
      "name":"Sagar",
    }
    return HttpResponse(res(1, message[1], args))
  else:
    return HttpResponse(res(0, message[0]))

@csrf_exempt
@api_view(['GET'])
def connect_camera(request):
  if request.method=="GET":
    meraki_api.connect_camera()
    return HttpResponse(res(1, message[1]))
  else:
    return HttpResponse(res(0, message[0]))


@csrf_exempt
@api_view(['GET'])
def disconnect_camera(request):
  if request.method=="GET":
    meraki_api.disconnect()
    return HttpResponse(res(1, message[1]))
  else:
    return HttpResponse(res(0, message[0]))

@csrf_exempt
@api_view(['GET'])
def do_recognition(request):
    if request.method == 'GET':
        known_names, known_face_encodings = face_recognition.scan_known_people(face_recognition.known_people_folder, isPresent)
        if sys.version_info < (3, 4) and cpus != 1:
            args = {
                'warning': "WARNING: Python 3.4+ is needed for multi-processing. Doing on single CPU",
                cpus: 1,
        }
        HttpResponse(res(0, message[0], args))
        # ?? ret already returning dict ??
        ret = face_recognition.test_image(face_recognition.images_to_check, known_names, known_face_encodings, tolerance, show_distance)
        return HttpResponse(res(1, message[1], ret))
    else:
        return HttpResponse(res(0, message[0]))


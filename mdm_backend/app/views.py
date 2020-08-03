import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .meraki_api import meraki_api
from .face_recognition import api, face_recognition
from .models import *
# Create your views here.

message = ["FAILURE", "SUCCESS", 'NOT_FOUND']

def format_response(data):
  return HttpResponse(
      serializers.serialize("json", data),
      content_type="text/json-comment-filtered"
  )

def res(status, message, data = None):
  # data = json.dumps(data)
  print(data, "dumped")
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
    data = meraki_api.disconnect()
    # sch = School.objects.filter(email='sagarbansal099@gmail.com').first()
    # dt = DailyPrediction()
    # dt.school = sch
    # print(data)
    # dt.attendance_true = data[len(data) - 1]['person_count']
    # dt.food_true = "Rice Dal"
    # dt.save()
    # report = Reports()
    # report.school = sch
    # report.pred = dt
    # report.save()
    return HttpResponse(res(1, message[1], data))
  else:
    return HttpResponse(res(0, message[0]))

@csrf_exempt
@api_view(['GET'])
def get_urls(request):
  if request.method=="GET":
    data = meraki_api.get_urls()
    return HttpResponse(res(1, message[1], data))
  else:
    return HttpResponse(res(0, message[0]))


@csrf_exempt
@api_view(['GET'])
def do_recognition(request):
    if request.method == 'GET':
      img =  {}
      known_names, known_face_encodings = face_recognition.scan_known_people(img, True)
      args = {}
      HttpResponse(res(0, message[0], args))
      # ?? ret already returning dict ??
      ret = face_recognition.test_image(face_recognition.images_to_check, known_names, known_face_encodings, tolerance, show_distance)
      # ret = {}
      return HttpResponse(res(1, message[1], ret))
    else:
        return HttpResponse(res(0, message[0]))

@csrf_exempt
@api_view(['POST'])
def add_attendance(request):
  if request.method == 'POST':
    data = request.data['data']['data']
    print(data)
    sch = School.objects.filter(email= 'sagarbansal099@gmail.com').first()
    dt = DailyTrue()
    dt.school = sch
    dt.attendance_true = data['attendance']
    dt.food_true = data['food']
    dt.save()
    return HttpResponse(res(1, message[1], dt.id))
  else:
    return HttpResponse(res(0, message[0]))

@csrf_exempt
@api_view(['GET'])
def get_reports(request):
  if request.method=="GET":
    data = meraki_api.get_urls()
    return HttpResponse(res(1, message[1], data))
  else:
    return HttpResponse(res(0, message[0]))

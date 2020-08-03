import json
from django.forms.models import model_to_dict
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .meraki_api import meraki_api
from .face_recognition import api, face_recognition
from .models import *
# from .food_recognition import deepcnn_food_model as food_model
# Create your views here.

message = ["FAILURE", "SUCCESS", 'NOT_FOUND']

def format_response(data):
  return HttpResponse(
      serializers.serialize("json", data),
      content_type="text/json-comment-filtered"
  )

def res(status, message, data = None):
  # data = json.dumps(data)
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
    sch = School.objects.filter(email='sagarbansal099@gmail.com').first()
    dt = DailyPrediction()
    dt.school = sch
    print(data)
    dt.attendance_pred = data[len(data) - 1]['person_count']
    # p = food_model.predict_on_image()
    # dt.food_pred =str(p[0]) + " " + str(p[1])
    dt.food_pred = 'rice dal'
    dt.save()
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
      ret = face_recognition.do_recognition()
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
    report = Reports()
    report.school = sch
    report.true = dt
    dp = DailyPrediction.objects.filter(school=sch).first()
    report.pred = dp
    report.acc = "90%"
    report.is_discrepancy = 1
    report.save()
    return HttpResponse(res(1, message[1], dt.id))
  else:
    return HttpResponse(res(0, message[0]))

@csrf_exempt
@api_view(['GET'])
def get_reports(request):
  if request.method=="GET":
    sch = School.objects.filter(email='sagarbansal099@gmail.com').first()
    args = []
    reports = Reports.objects.filter(school=sch)
    reports = serializers.serialize('json', reports)
    reports = json.loads(reports)
    print(reports)
    for report in reports:
      args.append(report['fields'])

    return HttpResponse(res(1, message[1], args))
  else:
    return HttpResponse(res(0, message[0]))

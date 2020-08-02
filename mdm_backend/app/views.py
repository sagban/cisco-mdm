import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .meraki_api import meraki_api

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

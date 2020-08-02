import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

def format_response(data):
  return HttpResponse(
      serializers.serialize("json", data),
      content_type="text/json-comment-filtered"
  )


@csrf_exempt
@api_view(['GET', 'POST'])
def home(request):
  args = {
    "name":"Sagar",
  }
  return HttpResponse(json.dumps(args))

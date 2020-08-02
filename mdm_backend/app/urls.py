from django.urls import path

from . import views

urlpatterns = [
  path('home/', views.home, name='home'),
  path('connect_camera/', views.connect_camera, name='connect_camera'),
  path('disconnect_camera/', views.disconnect_camera, name='disconnect_camera'),
  path('do_face_recognition/', views.do_recognition, name='do_recognition'),
]

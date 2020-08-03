from django.urls import path

from . import views

urlpatterns = [
  path('home/', views.home, name='home'),
  path('connect_camera/', views.connect_camera, name='connect_camera'),
  path('disconnect_camera/', views.disconnect_camera, name='disconnect_camera'),
  path('get_urls/', views.get_urls, name='get_urls'),
  path('do_face_recognition/', views.do_recognition, name='do_recognition'),
  path('add_attendance/', views.add_attendance, name='add_attendance'),
  path('get_reports/', views.get_reports, name='get_reports'),
]

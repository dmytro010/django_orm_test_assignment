from django.urls import path
from . import views


urlpatterns = [
    path('task1/', views.task_1_view),
    path('task2/', views.task_2_view),
    path('task3/', views.task_3_view),
    path('task4/', views.task_4_view),
    path('task5/', views.task_5_view),
    path('task6/', views.task_6_view),
]

from django.urls import path

from phonebillsapi.api.views.call_record_view import CallRecordView


urlpatterns = [
    path('callrecord/', CallRecordView.as_view(), name='callrecord')
]

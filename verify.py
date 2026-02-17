import os
import uuid
from datetime import datetime

# Django setup
from django.conf import settings

settings.configure(

    DEBUG=True,

    SECRET_KEY='secret',

    ROOT_URLCONF=__name__,

    ALLOWED_HOSTS=['*'],

    INSTALLED_APPS=[

        'rest_framework',

    ],

)

import django
django.setup()

# MongoEngine setup
from mongoengine import connect, Document, EmbeddedDocument
from mongoengine import StringField, DateTimeField
from mongoengine import EmbeddedDocumentField, DictField


connect(

    db="enterprise_logs_db",
    host="localhost",
    port=27017

)

# ----------------------------
# MODEL
# ----------------------------

class Metadata(EmbeddedDocument):

    ip_address = StringField()

    user_id = StringField()

    extra_data = DictField()


class Log(Document):

    log_id = StringField(

        primary_key=True,

        default=lambda: str(uuid.uuid4())

    )

    timestamp = DateTimeField(

        default=datetime.utcnow

    )

    service_name = StringField(

        required=True,

        index=True

    )

    log_level = StringField(

        index=True

    )

    message = StringField()

    metadata = EmbeddedDocumentField(

        Metadata

    )

    meta = {

        "collection": "logs",

        "indexes": [

            "service_name",

            "log_level",

            "timestamp"

        ]

    }


# ----------------------------
# SERIALIZER
# ----------------------------

from rest_framework import serializers


class LogSerializer(serializers.Serializer):

    log_id = serializers.CharField(read_only=True)

    timestamp = serializers.DateTimeField(read_only=True)

    service_name = serializers.CharField()

    log_level = serializers.CharField()

    message = serializers.CharField()

    metadata = serializers.DictField()


# ----------------------------
# SERVICE LAYER
# ----------------------------

class LogService:


    @staticmethod
    def create(data):

        metadata = Metadata(

            ip_address=data["metadata"].get("ip_address"),

            user_id=data["metadata"].get("user_id"),

            extra_data=data["metadata"].get("extra_data", {})

        )

        log = Log(

            service_name=data["service_name"],

            log_level=data["log_level"],

            message=data["message"],

            metadata=metadata

        )

        log.save()

        return log


    @staticmethod
    def get(service_name=None):

        if service_name:

            return Log.objects(service_name=service_name)

        return Log.objects()


    @staticmethod
    def update(log_id, data):

        log = Log.objects.get(log_id=log_id)

        log.update(**data)


    @staticmethod
    def delete(log_id):

        Log.objects.get(log_id=log_id).delete()


# ----------------------------
# VIEW
# ----------------------------

from rest_framework.views import APIView
from rest_framework.response import Response


class LogAPI(APIView):


    def post(self, request):

        log = LogService.create(request.data)

        return Response({

            "status": "created",

            "log_id": log.log_id

        })


    def get(self, request):

        service = request.GET.get("service_name")

        logs = LogService.get(service)

        data = LogSerializer(logs, many=True).data

        return Response(data)


    def put(self, request):

        LogService.update(

            request.data["log_id"],

            request.data

        )

        return Response({

            "status": "updated"

        })


    def delete(self, request):

        LogService.delete(

            request.data["log_id"]

        )

        return Response({

            "status": "deleted"

        })


# ----------------------------
# URL
# ----------------------------

from django.urls import path


urlpatterns = [

    path('logs/', LogAPI.as_view()),

]


# ----------------------------
# RUN SERVER
# ----------------------------

from django.core.management import execute_from_command_line

if __name__ == "__main__":

    execute_from_command_line(
        ["manage.py", "runserver"]
    )

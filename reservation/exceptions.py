from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import ugettext_lazy as _


class RecordOverlap(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('This record can not be allowed, '
                       'because overlap with existing allowed records')
    default_code = 'record overlap'

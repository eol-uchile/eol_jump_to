from django.conf.urls import url
from django.conf import settings

from .views import eol_jump_to

urlpatterns = (
    url(
        r'^courses/{}/eol_jump_to/(?P<location>.*)$'.format(
            settings.COURSE_ID_PATTERN,
        ),
        eol_jump_to,
        name='eol_jump_to',
    ),
)

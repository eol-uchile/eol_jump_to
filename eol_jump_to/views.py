# -*- coding: utf-8 -*-

from opaque_keys.edx.keys import CourseKey, UsageKey
from opaque_keys import InvalidKeyError

from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie

from lms.djangoapps.courseware.url_helpers import get_redirect_url
from xmodule.modulestore.exceptions import ItemNotFoundError, NoPathToItem

from openedx.features.course_experience import course_home_url_name

@ensure_csrf_cookie
def eol_jump_to(request, course_id, location):
    """
    EOL UPDATE: If item not found redirect to course home page
    Show the page that contains a specific location.
    If the location is invalid or not in any class, return a 404.
    Otherwise, delegates to the index view to figure out whether this user
    has access, and what they should see.
    """
    try:
        course_key = CourseKey.from_string(course_id)
        usage_key = UsageKey.from_string(location).replace(course_key=course_key)
    except InvalidKeyError:
        raise Http404(u"Invalid course_key or usage_key")
    try:
        redirect_url = get_redirect_url(course_key, usage_key, request)
    except ItemNotFoundError:
        # If item not found redirect to course home page
        redirect_url = reverse(course_home_url_name(course_key), kwargs={'course_id': course_id})
    except NoPathToItem:
        raise Http404(u"This location is not in any class: {0}".format(usage_key))
    return redirect(redirect_url)

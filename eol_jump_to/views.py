# -*- coding: utf-8 -*-

from django.views.generic.base import View
from django.http import HttpResponseRedirect

import logging
logger = logging.getLogger(__name__)

class EolJumpToView(View):
    def get(self, request):
        redirect = "https://stackoverflow.com/"
        return HttpResponseRedirect(redirect)

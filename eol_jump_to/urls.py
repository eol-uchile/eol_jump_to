from django.conf.urls import url
from django.conf import settings

from .views import EolJumpToView

urlpatterns = (
    url(
        r'eol_jump_to$',
        EolJumpToView.as_view(),
        name='eol_jump_to_view',
    ),
)

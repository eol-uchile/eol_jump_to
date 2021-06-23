
# coding=UTF-8


import six
from six import text_type
from six.moves.urllib.parse import urlencode

import ddt
from django.conf import settings
from django.test import RequestFactory
from django.test.client import Client
from django.urls import reverse
from opaque_keys.edx.keys import CourseKey, UsageKey
from opaque_keys.edx.locator import BlockUsageLocator, CourseLocator

from openedx.features.course_experience.url_helpers import get_courseware_url
from common.djangoapps.student.tests.factories import UserFactory
from xmodule.modulestore.tests.django_utils import (
    TEST_DATA_MIXED_MODULESTORE,
    ModuleStoreTestCase
)
from xmodule.modulestore.tests.factories import CourseFactory, ItemFactory

@ddt.ddt
class TestEolJumpTo(ModuleStoreTestCase):
    """
    Check the jumpto link for a course.
    """
    MODULESTORE = TEST_DATA_MIXED_MODULESTORE

    def setUp(self):
        super(TestEolJumpTo, self).setUp()
        # Use toy course from XML
        self.course_key = CourseKey.from_string('edX/toy/2012_Fall')

    def test_jumpto_invalid_location(self):
        location = self.course_key.make_usage_key(None, 'NoSuchPlace')
        # This is fragile, but unfortunately the problem is that within the LMS we
        # can't use the reverse calls from the CMS
        jumpto_url = '{0}/{1}/eol_jump_to/{2}'.format('/courses', six.text_type(self.course_key), six.text_type(location))
        response = self.client.get(jumpto_url)
        # self.assertEqual(response.status_code, 404) # jump_to original version
        self.assertEqual(response.status_code, 302) # eol_jump_to modification

    def test_jumpto_from_section(self):
        course = CourseFactory.create()
        chapter = ItemFactory.create(category='chapter', parent_location=course.location)
        section = ItemFactory.create(category='sequential', parent_location=chapter.location)
        expected = '/courses/{course_id}/courseware/{chapter_id}/{section_id}/?{activate_block_id}'.format(
            course_id=six.text_type(course.id),
            chapter_id=chapter.url_name,
            section_id=section.url_name,
            activate_block_id=urlencode({'activate_block_id': six.text_type(section.location)})
        )
        jumpto_url = '{0}/{1}/eol_jump_to/{2}'.format(
            '/courses',
            six.text_type(course.id),
            six.text_type(section.location),
        )
        response = self.client.get(jumpto_url)
        self.assertRedirects(response, expected, status_code=302, target_status_code=302)

    def test_jumpto_from_module(self):
        course = CourseFactory.create()
        chapter = ItemFactory.create(category='chapter', parent_location=course.location)
        section = ItemFactory.create(category='sequential', parent_location=chapter.location)
        vertical1 = ItemFactory.create(category='vertical', parent_location=section.location)
        vertical2 = ItemFactory.create(category='vertical', parent_location=section.location)
        module1 = ItemFactory.create(category='html', parent_location=vertical1.location)
        module2 = ItemFactory.create(category='html', parent_location=vertical2.location)

        expected = '/courses/{course_id}/courseware/{chapter_id}/{section_id}/1?{activate_block_id}'.format(
            course_id=six.text_type(course.id),
            chapter_id=chapter.url_name,
            section_id=section.url_name,
            activate_block_id=urlencode({'activate_block_id': six.text_type(module1.location)})
        )
        jumpto_url = '{0}/{1}/eol_jump_to/{2}'.format(
            '/courses',
            six.text_type(course.id),
            six.text_type(module1.location),
        )
        response = self.client.get(jumpto_url)
        self.assertRedirects(response, expected, status_code=302, target_status_code=302)

        expected = '/courses/{course_id}/courseware/{chapter_id}/{section_id}/2?{activate_block_id}'.format(
            course_id=six.text_type(course.id),
            chapter_id=chapter.url_name,
            section_id=section.url_name,
            activate_block_id=urlencode({'activate_block_id': six.text_type(module2.location)})
        )
        jumpto_url = '{0}/{1}/eol_jump_to/{2}'.format(
            '/courses',
            six.text_type(course.id),
            six.text_type(module2.location),
        )
        response = self.client.get(jumpto_url)
        self.assertRedirects(response, expected, status_code=302, target_status_code=302)

    def test_jumpto_from_nested_module(self):
        course = CourseFactory.create()
        chapter = ItemFactory.create(category='chapter', parent_location=course.location)
        section = ItemFactory.create(category='sequential', parent_location=chapter.location)
        vertical = ItemFactory.create(category='vertical', parent_location=section.location)
        nested_section = ItemFactory.create(category='sequential', parent_location=vertical.location)
        nested_vertical1 = ItemFactory.create(category='vertical', parent_location=nested_section.location)
        # put a module into nested_vertical1 for completeness
        ItemFactory.create(category='html', parent_location=nested_vertical1.location)
        nested_vertical2 = ItemFactory.create(category='vertical', parent_location=nested_section.location)
        module2 = ItemFactory.create(category='html', parent_location=nested_vertical2.location)

        # internal position of module2 will be 1_2 (2nd item withing 1st item)
        expected = '/courses/{course_id}/courseware/{chapter_id}/{section_id}/1?{activate_block_id}'.format(
            course_id=six.text_type(course.id),
            chapter_id=chapter.url_name,
            section_id=section.url_name,
            activate_block_id=urlencode({'activate_block_id': six.text_type(module2.location)})
        )
        jumpto_url = '{0}/{1}/eol_jump_to/{2}'.format(
            '/courses',
            six.text_type(course.id),
            six.text_type(module2.location),
        )
        response = self.client.get(jumpto_url)
        self.assertRedirects(response, expected, status_code=302, target_status_code=302)


    @ddt.data(
        (False, '1'),
        (True, '2')
    )
    @ddt.unpack
    def test_jump_to_for_learner_with_staff_only_content(self, is_staff_user, position):
        """
        Test for checking correct position in redirect_url for learner when a course has staff-only units.
        """
        course = CourseFactory.create()
        request = RequestFactory().get('/')
        request.user = UserFactory(is_staff=is_staff_user, username="staff")
        request.session = {}
        course_key = CourseKey.from_string(six.text_type(course.id))
        chapter = ItemFactory.create(category='chapter', parent_location=course.location)
        section = ItemFactory.create(category='sequential', parent_location=chapter.location)
        __ = ItemFactory.create(category='vertical', parent_location=section.location)
        staff_only_vertical = ItemFactory.create(category='vertical', parent_location=section.location,
                                                 metadata=dict(visible_to_staff_only=True))
        __ = ItemFactory.create(category='vertical', parent_location=section.location)

        usage_key = UsageKey.from_string(six.text_type(staff_only_vertical.location)).replace(course_key=course_key)
        expected_url = reverse(
            'courseware_position',
            kwargs={
                'course_id': six.text_type(course.id),
                'chapter': chapter.url_name,
                'section': section.url_name,
                'position': position,
            }
        )
        expected_url += "?{}".format(urlencode({'activate_block_id': six.text_type(staff_only_vertical.location)}))

        self.assertEqual(expected_url, get_courseware_url(usage_key, request))
#!/bin/dash

pip install -e /openedx/requirements/eol_jump_to

cd /openedx/requirements/eol_jump_to/eol_jump_to
cp /openedx/edx-platform/setup.cfg .
mkdir test_root
cd test_root/
ln -s /openedx/staticfiles .

cd /openedx/requirements/eol_jump_to/eol_jump_to

DJANGO_SETTINGS_MODULE=lms.envs.test EDXAPP_TEST_MONGO_HOST=mongodb pytest tests.py

rm -rf test_root

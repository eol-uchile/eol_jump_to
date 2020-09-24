# EOL JUMP TO (duplicate of edX jump_to)

![https://github.com/eol-uchile/eol_jump_to/actions](https://github.com/eol-uchile/eol_jump_to/workflows/Python%20application/badge.svg)

Redirect student to specific block if has access. Otherwise redirect to course index. 

## Install

    docker-compose exec lms pip install -e /openedx/requirements/eol_jump_to

## Use

Edit *lms/templates/dashboard.html*.

    resume_button_url = resume_button_urls[dashboard_index].replace("/jump_to/", "/eol_jump_to/")

## TESTS
**Prepare tests:**

    > cd .github/
    > docker-compose run --rm lms /openedx/requirements/eol_jump_to/.github/test.sh
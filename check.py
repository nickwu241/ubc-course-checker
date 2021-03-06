#!/usr/bin/env python
import os
import sys
import time

import requests
from twilio.rest import Client

COURSES_TO_CHECK = [
    'COMM 473 921'
]
SHOULD_SEND_TEXT_MESSAGE = True

TWILIO_FROM_NUMBER = os.environ['TWILIO_FROM_NUMBER']
TWILIO_TO_NUMBER = os.environ['TWILIO_TO_NUMBER']
TWILIO_CLIENT = Client(
    os.environ['TWILIO_ACCOUNT_SID'],
    os.environ['TWILIO_AUTH_TOKEN']
)

def __send_course_request(dept_name, course_name, section, sesscd='S', sessyr=2019):
    return requests.get('https://courses.students.ubc.ca/cs/courseschedule', params={
        'pname': 'subjarea',
        'tname': 'subj-section',
        'dept': dept_name,
        'course': course_name,
        'section': section,
        'sesscd': sesscd,
        'sessyr': sessyr,
    })

def __send_text(content, should_send_text=True):
    if should_send_text:
        TWILIO_CLIENT.messages.create(
            body=content,
            from_=TWILIO_FROM_NUMBER,
            to=TWILIO_TO_NUMBER
        )
    print(f'sent text message: {content}')

def check_courses():
    print(f'checking spots for {COURSES_TO_CHECK}...')
    for course in list(COURSES_TO_CHECK):
        resp = __send_course_request(*course.split())
        resp.raise_for_status()
        course_is_full = 'Note: this section is full' in resp.text
        if course_is_full:
            print(f'{course} is full :(')
        else:
            __send_text(
                f'{course} has a free spot! Register at {resp.url}',
                should_send_text=SHOULD_SEND_TEXT_MESSAGE)
            COURSES_TO_CHECK.remove(course)

def handler(event, context):
    check_courses()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        __send_text('TEST MESSAGE')
        exit(0)

    while True:
        check_courses()
        if not COURSES_TO_CHECK:
            break
        time.sleep(300)

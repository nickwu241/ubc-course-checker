#!/usr/bin/env python
import os
import time

import requests
from twilio.rest import Client

COURSES_TO_CHECK = [
    'LING 447G 001'
]

TWILIO_FROM_NUMBER = os.environ['TWILIO_FROM_NUMBER']
TWILIO_TO_NUMBER = os.environ['TWILIO_TO_NUMBER']
TWILIO_CLIENT = Client(
    os.environ['TWILIO_ACCOUNT_SID'],
    os.environ['TWILIO_AUTH_TOKEN']
)

def __send_course_request(dept_name, course_name, section):
    return requests.get('https://courses.students.ubc.ca/cs/main', params={
        'pname': 'subjarea',
        'tname': 'subjarea',
        'req': '5',
        'dept': dept_name,
        'course': course_name,
        'section': section
    })

def __send_text(content):
    TWILIO_CLIENT.messages.create(
        body=content,
        from_=TWILIO_FROM_NUMBER,
        to=TWILIO_TO_NUMBER
    )
    print(content)

def check_courses():
    print(f'checking spots for {COURSES_TO_CHECK}...')
    for course in list(COURSES_TO_CHECK):
        resp = __send_course_request(*course.split())
        resp.raise_for_status()
        course_is_full = 'Note: this section is full' in resp.text
        if course_is_full:
            print(f'{course} is full :(')
        else:
            __send_text(f'{course} has a free spot! Register at {resp.url}')
            COURSES_TO_CHECK.remove(course)

def handler(event, context):
    check_courses()

if __name__ == '__main__':
    while True:
        check_courses()
        if not COURSES_TO_CHECK:
            break
        time.sleep(300)

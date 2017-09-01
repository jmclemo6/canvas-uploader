import os
import sys
import json
from os.path import isfile

import requests

try:
    import config
except ImportError:
    sys.exit("Unable to load configuration file. See README for more information")

# Create module-wide authenticated session
auth_session = requests.Session()
auth_session.headers = {
    'Authorization': 'Bearer {0}'.format(
        config.auth_token)}


def get_course():
    try:
        response = auth_session.get(
            ''.join([config.domain, '/api/v1/courses']))
    finally:
        auth_session.close()
    
    latestTerm = 0
    for i in range(len(response.json())):
        if 'enrollment_term_id' in response.json()[i] and response.json()[i]['enrollment_term_id'] > latestTerm:
            latestTerm = response.json()[i]['enrollment_term_id']

    courses = list(
        filter(
            lambda a: 'enrollment_term_id' in a and a['enrollment_term_id'] >= latestTerm and 'name' in a,
            response.json()))

    for i in range(len(courses)):
        print("[{0}] {1}".format(i + 1, courses[i]['name']))

    selection = int(input("Select Course: ")) - 1

    return courses[selection]['id']


def get_assignment(class_id):
    url = ''.join(
        [config.domain, '/api/v1/courses/{0}/assignments'.format(class_id)])
    params = {'include': ['submission']}
    try:
        response = auth_session.get(url, params=params)
    finally:
        auth_session.close()
    assignments = list(
        filter(
            lambda a: 'online_upload' in a['submission_types'] and a['locked_for_user'] != True,
            response.json()))

    print()
    if not assignments:
        print("This class has no assignments aviliable for you.")
        return None
    for i in range(len(assignments)):
        print("[{0}] {1}".format(i + 1, assignments[i]['name']))

    selection = int(input("Select assignment: ")) - 1
    
    if 'submission' in assignments[selection]:
        choice = ""
        while choice != "n" and choice != "y":
            choice = input("This assignment already has a submisson. Continue? [y/n]: ")
        if choice.lower() == "n":
            return None

    return assignments[selection]['id']


def get_file():
    cwd = os.getcwd()
    files = list(filter(isfile, os.listdir(cwd)))

    if not files:
        print("No files to upload in current directory.")
        return None;
    print()
    for i in range(len(files)):
        print("[{0}] {1}".format(i + 1, files[i]))

    selection = int(input("Select file: ")) - 1

    return files[selection]

import os
from os.path import join, dirname
from dotenv import load_dotenv
import json
import jenkins

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

jenkins_api_build_info_depth = 2
change_file_name = '.last_data.json'

def login_jenkins():
    jenkins_url = 'http://localhost:8080'
    JENKINS_USER = os.environ.get('JENKINS_USER')
    JENKINS_PASS = os.environ.get('JENKINS_PASS')

    server = jenkins.Jenkins(jenkins_url, username=JENKINS_USER, password=JENKINS_PASS)
    user = server.get_whoami()
    version = server.get_version()
    print('Hello %s from Jenkins %s' % (user['fullName'], version))
    return server


def get_current_info(jenkins_server):
    last_build = jenkins_server.get_job_info('test')
    build_info = jenkins_server.get_build_info('test',
        last_build['lastCompletedBuild']['number'], jenkins_api_build_info_depth)
    return [last_build, build_info]


def update_changes_file(data):
    with open(change_file_name, 'w') as outfile:
        json.dump(data, outfile)


def get_last_change():
    with open(change_file_name) as f:
        data = json.load(f)
        return data
    return {}


def compute_build_info_actions(build_info):
    if build_info['building'] == True:
        raise Exception('Still building')

    


def compare_to_last(last_build, build_info, jenkins_server):
    last_notification = get_last_change()
    differences_result = []
    complete = False
    while(complete == False):
        if last_build['lastCompletedBuild']['number'] != last_notification['lastBuildNumber']:

            build_info = jenkins_server.get_build_info('test',
                last_notification['lastBuildNumber'], jenkins_api_build_info_depth)

            if build_info['result'] != last_notification['lastBuildResult']:
                last_notification['lastBuildResult'] = build_info['result']
                differences_result.append(['test', build_info['actions'][0]['causes'][0]['shortDescription']])

            else:
                return ['test', build_info['actions'][2]['causes'][0]['shortDescription']]

        elif build_info['result'] != last_notification['lastBuildResult']:
            return ['test', build_info['actions'][0]['causes'][0]['shortDescription']]
    
    return differences_result


def verify_changes():
    jenkins_server = login_jenkins()
    [last_build, build_info] = get_current_info(jenkins_server)
    comparison_result = compare_to_last(last_build, build_info, jenkins_server)
    return comparison_result[0] + ',' + comparison_result[1]


print(verify_changes())


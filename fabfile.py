from fabric.decorators import task
from fabric.operations import local


@task
def runserver():
    start_redis()
    local('gunicorn --config url_shortner/gunicorn_conf.py url_shortner.wsgi:app &')


@task
def stop_server():
    stop_redis()
    local("ps -ef | grep gunicorn | grep -v grep | awk '{print $2}' | xargs kill")


@task
def run_unit_tests():
    local('nosetests test/unit/')


@task
def run_acceptance_tests():
    local('behave test/acceptance/features --no-capture')


@task
def start_redis():
    local('redis-server &')


def stop_redis():
    local('redis-cli shutdown')


@task
def build():
    run_unit_tests()
    start_redis()
    run_acceptance_tests()
    stop_redis()
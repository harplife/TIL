from flask import Flask
import time
import requests
import atexit

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

app = Flask(__name__)

job_defaults = {
    'max_instances': 3,  # this is for short interval tasks
    # 'replace_existing': True,
    # 'coalesce': False,
    # 'misfire_grace_time': 15*60
}

jobstores = {
    # sqlite db will be created if not exists
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.db')
}

# here we define our scheduler, which wont start without start()
sched = BackgroundScheduler(jobstores = jobstores, job_defaults=job_defaults)

def jobs_manager(func):
    '''Context Manager for scheduling jobs.'''
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(e)
        else:
            pass
    return wrapper

def job1():
    print(f'job1 : {time.strftime("%H:%M:%S")}')

def job2():
    print(f'job2 : {time.strftime("%H:%M:%S")}')

def job3():
    url = 'http://localhost:8003/'
    with requests.Session() as s:
        r = s.get(url)
        if r.status_code != 200:
            print(f'{r.status_code} error!')
        else:
            print(f'job3 : {time.strftime("%H:%M:%S")}')

# this starts the scheduler
sched.start()

# make sure jobs are added after the scheduler starts,
# this makes sure that exceptions are handled on adding, not starting

# job at every 10 seconds (from starting point)
jobs_manager(sched.add_job)(job1, 'interval', seconds=10, id='test_1')
# job at 12:30
jobs_manager(sched.add_job)(job2, 'cron', hour='12', minute='30', id='test_2')
# job at every minute (hh:mm:00)
jobs_manager(sched.add_job)(job2, 'cron', second='0', id='test_3')
# job at every 15 seconds
jobs_manager(sched.add_job)(job3, 'interval', seconds=15, id='test_4')


@app.route('/')
def index():
    return "<h1>testing</h1>"


@app.route('/jobs')
def jobs():
    # prints pending jobs
    sched.print_jobs()
    return "<h1>Check the terminal</h1>"


if __name__ == '__main__':
    atexit.register(sched.remove_all_jobs)  # shutdown jobs, and jobs on jobstore
    #atexit.register(sched.shutdown)  # shutsdown jobs, but leaves jobstore alone
    app.run(port=8003, threaded=True)

import sys
from celery import Celery
import time
import os

celery_app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

def write_error_log(error, filename='write_errors.txt', directory=None,  date=None):
    target = 'error_log'
    import datetime
    if not os.path.isdir(target):
        os.mkdir(target)

    if directory:
        path = os.path.join(target, directory)
        filename = os.path.join(path, filename)
        if not os.path.isdir(path):
            if not os.path.isdir(target):
                os.mkdir(target)
            os.mkdir(path)
    else:
        filename = os.path.join(target, filename)
    try:
        with open(filename, 'a') as file:
            file.write("\n" + str(error) + ' ~ ' + str(date if date else datetime.datetime.utcnow()))
    except Exception as e:
        print(e)

@celery_app.task
def compute_risk_score_task(data):
    try:
        score = 0
        breakdown = []

        if data['region'].lower() == 'eu' and data['data_sensitivity'].lower() == 'high':
            score += 30
            breakdown.append("High sensitivity data in EU: +30")

        if data['processor'] == 'UnknownVendor':
            score += 20
            breakdown.append("Untrusted processor: +20")

        if data['purpose'].lower() == 'marketing':
            score += 15
            breakdown.append("Purpose is marketing: +15")

        time.sleep(2)
        return {
            "risk_score": min(score, 100),
            "breakdown": breakdown
        }
    except Exception as e:
        print(e)
        exception_type, exception_object, exception_traceback = sys.exc_info()
        errorFilename = exception_traceback.tb_frame.f_code.co_filename
        line_number = exception_traceback.tb_lineno
        error = {
            'error': str(e),
            'Line Number': str(line_number),
            'File': str(errorFilename)
        }
        print(e)
        write_error_log('compute risk score task: ' + str(error), 'error_log.txt')

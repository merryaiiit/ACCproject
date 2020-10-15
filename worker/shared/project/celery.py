from celery import Celery
import os

app = Celery('project',
             broker='pyamqp://admin:admin@'+os.environ['RMQIP']+':5672//',
             backend='rpc://',
             include=['project.tasks'])

if __name__=='__main__':
    app.start()

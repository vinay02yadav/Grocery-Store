from celery import Celery
from celery.schedules import crontab
from flask import current_app as ap
from app.models import Login,db


celery = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0',
    include=["app.tasks"],  
)



# celery.conf.beat_schedule = {

#     # 'send-email-every-day': {
#     #     'task': 'app.tasks.send_email', 
#     #     'schedule': crontab(hour=10, minute=25), 
#     #     'options': {
#     #         'max_interval': 700,
#     #     },
#     # },
    
#     'Monthly Activity Report': {
#         'task': 'app.tasks.sendMonthlyMail', 
#         'schedule': crontab(hour=11, minute=29), 
#         'options': {
#             'max_interval': 700,
#         }, 
#     },
# }


celery.conf.timezone = 'Asia/Kolkata'  

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with ap.app_context():
            return self.run(*args, **kwargs)
        
        


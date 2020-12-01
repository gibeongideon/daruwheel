from celery import task 
from celery import shared_task 
# # We can have either registered task 
# @task(name='summary') 
# def send_import_summary():
#     pass
#      # Magic happens here ... 
# # or 
@shared_task 
def createwheelspininstance():
     print('Here Is ME')
     # Another trick
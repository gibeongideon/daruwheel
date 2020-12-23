from time import sleep
from celery import shared_task
from .functions import countC ,spin_manager


@shared_task 
def create_spinwheel():
    ''' wheel instance to be executed every 5 minutes'''
    print('At create_spinwheel periodic task') 
    spin_manager()
    # countD((4.5*60))
    print('SPIN SPIN!! ')


@shared_task
def start_count_down():
    ''' precise spin timer task'''
    sleep(16) # spin time then 
    countC(277) # kick up the timer   # 277 + 16 = 296 seconds = 4.8 minutes
    
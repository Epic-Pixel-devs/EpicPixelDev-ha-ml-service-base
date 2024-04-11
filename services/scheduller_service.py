# -*- coding: utf-8 -*-

from apscheduler.schedulers.background import BackgroundScheduler

from batches.valorant.main import initialize


class SchedulerService(BackgroundScheduler):
    def __init__(self):
        super().__init__()
        self.add_job(func=initialize, id='batch_valorant')

        self.reschedule_job('batch_valorant', trigger='cron', year='*', month='*', day='*',
                            week='*', day_of_week='*', hour=0, minute=30, second=0)

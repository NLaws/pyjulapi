# *********************************************************************************
# REopt, Copyright (c) 2019-2020, Alliance for Sustainable Energy, LLC.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this list
# of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice, this
# list of conditions and the following disclaimer in the documentation and/or other
# materials provided with the distribution.
#
# Neither the name of the copyright holder nor the names of its contributors may be
# used to endorse or promote products derived from this software without specific
# prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.
# *********************************************************************************
import os
import logging
from celery import Celery
from celery.signals import after_setup_logger


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pyapi.settings')

app = Celery('reopt_api')

# # Example of killing celery task:
# app.control.revoke('a879bf13-6689-41bc-bd23-ad6a05920f24', terminate=True)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# redis_host varies if running locally for debug or within containers
redis_host = os.environ.get('REDIS_HOST', 'localhost')
app.conf.broker_url = 'redis://' + redis_host + ':6379/0'

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@after_setup_logger.connect
def setup_loggers(logger, *args, **kwargs):
    # file_formatter = logging.Formatter(
    #     '%(asctime)s %(name)-12s %(levelname)-8s %(filename)s::%(funcName)s line %(lineno)s %(message)s')
    console_formatter = logging.Formatter(
        '%(name)-12s %(levelname)-8s %(filename)s::%(funcName)s line %(lineno)s %(message)s')

    # logfile = os.path.join(os.getcwd(), "log", "reopt_api.log")
    #
    # file_handler = logging.FileHandler(filename=logfile, mode='a')
    # file_handler.setFormatter(file_formatter)
    # file_handler.setLevel(logging.INFO)
    # logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

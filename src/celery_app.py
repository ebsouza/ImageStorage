import os

from celery import Celery
from kombu import Exchange, Queue

from src.config import get_rabbit_config

#Celery Setup
celery = Celery('worker-celery', broker=get_rabbit_config())

#Load config from a file
celery.config_from_object('src.celeryconfig')

#Load project tasks and create queues
tasks = []
queues = []
tasks_path = f"{os.getcwd()}/src/tasks"

files = os.listdir(tasks_path)
for task in files:
    if not task.startswith("_") and task.endswith(".py"):
        task = task.split(".")[0]
        tasks.append(f"src.tasks.{task}")

        queues.append(
            Queue(
                task,
                Exchange(task, type="direct"),
                routing_key=f"src.task.{task}",
                queue_arguments={"x-max-priority": 255},
            ), )
celery.conf.task_queues = queues
celery.autodiscover_tasks(tasks)

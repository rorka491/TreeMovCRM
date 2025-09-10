import subprocess
import signal
import os
from django.core.management.commands.runserver import Command as RunserverCommand


class Command(RunserverCommand):
    help = "Run Django dev server + Celery worker + beat"

    def handle(self, *args, **options):
        # Запускаем celery worker и beat только в основном процессе (не при autoreload)
        if os.environ.get("RUN_MAIN") != "true":
            self.celery_worker_proc = subprocess.Popen(
                ["celery", "-A", "tmcrm", "worker", "--loglevel=info"]
            )
            self.celery_beat_proc = subprocess.Popen(
                ["celery", "-A", "tmcrm", "beat", "--loglevel=info"]
            )
        else:
            self.celery_worker_proc = None
            self.celery_beat_proc = None

        try:
            super().handle(*args, **options)
        except KeyboardInterrupt:
            print("\nОстановка: завершаем Celery и сервер...")
        finally:
            if self.celery_worker_proc:
                self.celery_worker_proc.send_signal(signal.SIGINT)
                self.celery_worker_proc.wait()
            if self.celery_beat_proc:
                self.celery_beat_proc.send_signal(signal.SIGINT)
                self.celery_beat_proc.wait()

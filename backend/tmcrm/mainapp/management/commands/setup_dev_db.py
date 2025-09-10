from typing import Any
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Полный сетап базы данных для дальнейшей разработки'        

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write(self.style.NOTICE("Сбрасываю базу..."))
        call_command("flush", "--noinput")

        self.stdout.write(self.style.NOTICE("Миграции..."))
        call_command("migrate")

        self.stdout.write(self.style.NOTICE("Создаю суперюзера..."))
        call_command("createsuperuser", interactive=True)

        self.stdout.write(self.style.NOTICE("Загружаю фикстуры..."))
        call_command("loaddata", "initial_data.json")

        self.stdout.write(self.style.SUCCESS("✅ База готова для разработки"))
    

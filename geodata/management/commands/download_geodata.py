import os
import shutil
import gzip

from pathlib import Path

import requests
from django.core.management.base import BaseCommand, CommandError


STATES_URL = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/sqlite/states.sqlite3"
CITIES_GZ_URL = "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/sqlite/cities.sqlite3.gz"


class Command(BaseCommand):
    help = "Скачать и подготовить гео-базы (states.sqlite3, cities.sqlite3) в папку temp"

    def handle(self, *args, **options):
        base_dir = Path(os.getcwd())
        temp_dir = base_dir / "temp"

        # 1. Создать temp, если нет
        temp_dir.mkdir(parents=True, exist_ok=True)

        # 2. Удалить всё внутри temp
        self.stdout.write(f"Очистка папки: {temp_dir}")
        for item in temp_dir.iterdir():
            if item.is_file() or item.is_symlink():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)

        # 3. Скачиваем states.sqlite3
        states_path = temp_dir / "states.sqlite3"
        self.stdout.write(f"Скачивание states.sqlite3 в {states_path}")

        try:
            self._download_file(STATES_URL, states_path)
        except Exception as e:
            raise CommandError(f"Не удалось скачать states.sqlite3: {e}")

        # 4. Скачиваем cities.sqlite3.gz
        cities_gz_path = temp_dir / "cities.sqlite3.gz"
        cities_path = temp_dir / "cities.sqlite3"

        self.stdout.write(f"Скачивание cities.sqlite3.gz в {cities_gz_path}")

        try:
            self._download_file(CITIES_GZ_URL, cities_gz_path)
        except Exception as e:
            raise CommandError(f"Не удалось скачать cities.sqlite3.gz: {e}")

        # 5. Распаковка .gz -> .sqlite3
        self.stdout.write(f"Распаковка {cities_gz_path} в {cities_path}")
        try:
            with gzip.open(cities_gz_path, "rb") as f_in:
                with open(cities_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)
        except Exception as e:
            raise CommandError(f"Не удалось распаковать {cities_gz_path}: {e}")

        # Можно удалить .gz после распаковки
        try:
            cities_gz_path.unlink()
        except OSError:
            pass

        self.stdout.write(self.style.SUCCESS("Гео-базы успешно скачаны и подготовлены."))
        self.stdout.write(f"states: {states_path}")
        self.stdout.write(f"cities: {cities_path}")

    def _download_file(self, url: str, dest: Path, chunk_size: int = 8192):
        """Скачивает файл по URL с потоковой записью на диск."""
        resp = requests.get(url, stream=True, timeout=60)
        resp.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)

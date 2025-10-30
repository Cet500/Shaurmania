import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from ..utils.tree_utils import TreeBuilder


class Command(BaseCommand):
	help = "Полное удаление кэш-файлов проекта"

	def add_arguments(self, parser):
		parser.add_argument(
			"--noinput",
			"--no-input",
			action="store_true",
			dest="noinput",
			help="Автоматическое подтверждение удаления",
		)

	def get_pycache_dirs(self, base_dir):
		"""Рекурсивно ищет __pycache__ директории, исключая системные папки"""
		exclude_dirs = {'.venv', 'venv', '.git', '.idea'}
		pycache_dirs = []

		for pycache_dir in base_dir.rglob("__pycache__"):
			# Проверяем, не находится ли путь в исключенных директориях
			if any(exclude in pycache_dir.parts for exclude in exclude_dirs):
				continue
			pycache_dirs.append(pycache_dir)

		return pycache_dirs

	def handle(self, *args, **options):
		# Формируем список путей для удаления
		targets = []

		# Media cache
		if hasattr(settings, "MEDIA_ROOT"):
			media_cache = Path(settings.MEDIA_ROOT) / "CACHE"
			if media_cache.exists():
				targets.append(media_cache)

		# Pycache (исключая виртуальное окружение)
		base_dir = Path(settings.BASE_DIR)
		pycache_dirs = self.get_pycache_dirs(base_dir)
		targets.extend(pycache_dirs)

		# Pytest cache
		pytest_cache = base_dir / ".pytest_cache"
		if pytest_cache.exists():
			targets.append(pytest_cache)

		# Static cache
		if hasattr(settings, "STATIC_ROOT"):
			static_cache = Path(settings.STATIC_ROOT) / "CACHE"
			if static_cache.exists():
				targets.append(static_cache)

		# Фильтруем только существующие пути
		existing_targets = [t for t in targets if t.exists()]

		if not existing_targets:
			self.stdout.write("Кэш-файлы не найдены")
			return

		# Используем TreeBuilder для красивого вывода
		tree_builder = TreeBuilder(stdout=self.stdout, style=self.style)

		self.stdout.write("Найдены следующие кэш-директории:")

		# Выводим каждую цель в виде дерева
		for target in existing_targets:
			self.stdout.write(f"\n{target}:")
			if target.is_dir():
				tree = tree_builder.build_tree(target)
				tree_builder.print_tree(tree)
			else:
				self.stdout.write(f"  📄 {target.name}")

		# Подтверждение
		if not options["noinput"]:
			confirm = input("\nВы уверены? [y/n]: ")
			if not confirm.lower().startswith("y"):
				self.stdout.write("Отменено")
				return

		# Удаление
		deleted_count = 0
		for item in existing_targets:
			try:
				if item.is_dir():
					shutil.rmtree(item)
				else:
					item.unlink()
				self.stdout.write(f"Удалено: {item}")
				deleted_count += 1
			except Exception as e:
				self.stderr.write(f"Ошибка при удалении {item}: {e}")

		self.stdout.write(
			self.style.SUCCESS(f"Удалено {deleted_count} кэш-объектов из {len(existing_targets)}")
		)

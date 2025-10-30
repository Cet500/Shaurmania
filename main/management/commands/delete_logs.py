import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from ..utils.tree_utils import TreeBuilder, format_size


class Command( BaseCommand ):
	help = "Удаление логов проекта (требует подтверждения)"

	def add_arguments( self, parser ):
		parser.add_argument(
			"--noinput",
			"--no-input",
			action = "store_true",
			dest = "noinput",
			help = "Автоматическое подтверждение удаления",
		)
		parser.add_argument(
			"--keep-structure",
			action = "store_true",
			help = "Удалить только содержимое логов, но сохранить структуру папок",
		)

	def handle( self, *args, **options ):
		# Проверяем наличие LOG_DIR в настройках
		if not hasattr( settings, "LOG_DIR" ):
			self.stderr.write( self.style.ERROR( "LOG_DIR не найден в настройках проекта" ) )
			return

		log_dir = Path( settings.LOG_DIR )

		if not log_dir.exists():
			self.stdout.write( f"Директория логов не найдена: {log_dir}" )
			return

		# Используем TreeBuilder для отображения структуры
		tree_builder = TreeBuilder(stdout=self.stdout, style=self.style)

		# Подсчет статистики
		total_size, file_count, dir_count = tree_builder.calculate_stats(log_dir)

		if file_count == 0 and dir_count == 0:
			self.stdout.write( "Логи не найдены" )
			return

		# Вывод информации через TreeBuilder
		self.stdout.write( f"Директория логов: {log_dir}" )
		self.stdout.write( f"Найдено: {file_count} файлов, {dir_count} папок" )
		self.stdout.write( f"Общий размер: {format_size( total_size )}" )

		self.stdout.write( "\nСтруктура логов для удаления:" )

		# Построение и вывод дерева
		tree = tree_builder.build_tree(log_dir)
		tree_builder.print_tree(tree)

		# Подтверждение
		if not options["noinput"]:
			self.stdout.write( self.style.WARNING(
				"\n⚠️  ВНИМАНИЕ: Логи содержат важную информацию для отладки!"
			) )
			confirm = input( "Вы уверены что хотите удалить все логи? [y/N]: " )
			if not confirm.lower().startswith( "y" ):
				self.stdout.write( "Отменено" )
				return

		# Удаление
		deleted_files = 0
		deleted_dirs = 0
		deleted_size = 0

		for item in log_dir.rglob( '*' ):
			try:
				if item.is_file():
					file_size = item.stat().st_size
					item.unlink()
					deleted_size += file_size
					deleted_files += 1
				elif item.is_dir():
					if options["keep_structure"]:
						# Удаляем только содержимое папки
						for subitem in item.iterdir():
							if subitem.is_file():
								file_size = subitem.stat().st_size
								subitem.unlink()
								deleted_size += file_size
								deleted_files += 1
							else:
								shutil.rmtree( subitem )
								deleted_dirs += 1
					else:
						shutil.rmtree( item )
						deleted_dirs += 1
			except Exception as e:
				self.stderr.write( f"Ошибка при удалении {item}: {e}" )

		# Результаты
		self.stdout.write(
			self.style.SUCCESS(
				f"\nУдалено: {deleted_files} файлов, {deleted_dirs} папок "
				f"({format_size(deleted_size)})"
			)
		)

		if options["keep_structure"]:
			self.stdout.write( "Структура папок сохранена" )

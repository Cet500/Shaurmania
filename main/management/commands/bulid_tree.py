from pathlib import Path
from django.conf import settings
from django.core.management.base import BaseCommand
from ..utils.tree_utils import TreeBuilder, format_size


class Command( BaseCommand ):
	help = "Построение дерева файловой структуры с статистикой"

	def add_arguments( self, parser ):
		parser.add_argument(
			"dir",
			nargs = "?",
			default = ".",
			help = "Директория для построения дерева (по умолчанию - корень проекта)",
		)
		parser.add_argument(
			"--exclude",
			action="append",
			help="Паттерны для исключения из вывода (можно указать несколько)",
		)
		parser.add_argument(
			"--no-exclude-default",
			action="store_true",
			help="Не использовать исключения по умолчанию",
		)

	def handle( self, *args, **options ):
		target_dir = Path( options["dir"] )

		# Если указана относительная, считаем от BASE_DIR
		if not target_dir.is_absolute():
			target_dir = Path( settings.BASE_DIR ) / target_dir

		if not target_dir.exists():
			self.stderr.write( f"Ошибка: Директория {target_dir} не существует" )
			return

		if not target_dir.is_dir():
			self.stderr.write( f"Ошибка: {target_dir} не является директорией" )
			return

		# Формируем список исключений
		exclude_patterns = options["exclude"] or []
		if not options["no_exclude_default"]:
			# Уже есть стандартные исключения в TreeBuilder
			pass

		# Создаем построитель дерева
		tree_builder = TreeBuilder( stdout = self.stdout, style = self.style )

		# Подсчет статистики
		total_size, file_count, dir_count = tree_builder.calculate_stats(
			target_dir, exclude_patterns=exclude_patterns
		)

		# Вывод информации
		self.stdout.write( f"Директория: {target_dir}" )
		self.stdout.write( f"Найдено: {file_count} файлов, {dir_count} папок" )
		self.stdout.write(f"Общий размер: {format_size(total_size)}")

		self.stdout.write( "\nСтруктура:" )

		# Построение и вывод дерева
		tree = tree_builder.build_tree(target_dir, exclude_patterns=exclude_patterns)
		tree_builder.print_tree( tree )

		if not options["no_exclude_default"]:
			self.stdout.write(
				self.style.NOTICE("\n(технические папки исключены из вывода)")
			)

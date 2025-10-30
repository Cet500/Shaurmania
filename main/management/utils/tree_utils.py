from pathlib import Path


def format_size(size_in_bytes):
	"""
	Форматирует размер в байтах в читаемую строку (B, KB, MB, GB, TB)
	"""
	if size_in_bytes == 0:
		return "0 B"

	# Определяем единицы измерения
	units = ['B', 'KB', 'MB', 'GB', 'TB']
	unit_index = 0
	size = float(size_in_bytes)

	# Находим подходящую единицу измерения
	while size >= 1024.0 and unit_index < len(units) - 1:
		unit_index += 1
		size /= 1024.0

	# Определяем формат вывода в зависимости от размера
	if unit_index == 0:  # Байты
		return f"{int(size)} {units[unit_index]}"
	elif size < 10:  # Маленькие размеры - 2 знака после запятой
		return f"{size:.2f} {units[unit_index]}"
	elif size < 100:  # Средние размеры - 1 знак после запятой
		return f"{size:.1f} {units[unit_index]}"
	else:  # Большие размеры - целые числа
		return f"{int(size)} {units[unit_index]}"


class TreeBuilder:
	"""Утилита для построения дерева файловой структуры"""

	def __init__( self, stdout = None, style = None ):
		self.stdout = stdout
		self.style = style

	def should_exclude(self, path, exclude_patterns=None):
		"""Проверяет, нужно ли исключить путь из вывода"""
		if not exclude_patterns:
			exclude_patterns = []

		# Стандартные исключения для технических папок
		default_exclude = {
			'.venv', 'venv', '.git', '__pycache__', '.pytest_cache',
			'.mypy_cache', '.tox', '.eggs', '*.egg-info', 'build',
			'dist', '.cache', '.idea', '.vscode', 'node_modules'
		}

		all_exclude = default_exclude.union(set(exclude_patterns))

		# Проверяем каждую часть пути
		for part in path.parts:
			for pattern in all_exclude:
				if pattern in part or part == pattern:
					return True
		return False

	def calculate_stats(self, directory, exclude_patterns=None):
		"""Подсчитывает общую статистику по директории"""
		total_size = 0
		file_count = 0
		dir_count = 0

		for item in directory.rglob( '*' ):
			if self.should_exclude(item, exclude_patterns):
				continue

			if item.is_file():
				try:
					total_size += item.stat().st_size
					file_count += 1
				except OSError:
					pass
			elif item.is_dir():
				dir_count += 1

		return total_size, file_count, dir_count

	def build_tree(self, directory, exclude_patterns=None):
		"""Строит дерево файлов и папок для красивого вывода"""
		tree = { }

		for item in directory.rglob( '*' ):
			if self.should_exclude(item, exclude_patterns):
				continue

			try:
				relative_path = item.relative_to( directory )
				parts = relative_path.parts

				# Строим дерево
				current_level = tree
				for i, part in enumerate( parts ):
					if part not in current_level:
						if i == len( parts ) - 1:
							current_level[part] = {
								"_item": item,
								"_type": "dir" if item.is_dir() else "file"
							}
						else:
							current_level[part] = { }
					current_level = current_level[part]
			except (ValueError, PermissionError):
				continue

		return tree

	def print_tree( self, tree, indent = 0, is_last = True, prefix = "" ):
		"""Рекурсивно выводит дерево файлов с красивыми префиксами"""
		if not tree:
			return

		# Сортируем: сначала папки, потом файлы, всё по алфавиту
		sorted_items = sorted(
			[(key, value) for key, value in tree.items()
			 if key != "_item" and key != "_type"],
			key = lambda x: (
				not isinstance( x[1].get( '_item' ), Path ) or x[1].get( '_type' ) != 'dir',
				x[0].lower()
			)
		)

		for i, (name, subtree) in enumerate( sorted_items ):
			is_last_item = i == len( sorted_items ) - 1

			# Определяем префиксы для дерева
			if indent == 0:
				current_prefix = ""
				next_prefix = ""
			else:
				current_prefix = prefix + ("└── " if is_last else "├── ")
				next_prefix = prefix + ("    " if is_last else "│   ")

			item = subtree.get( '_item' )
			item_type = subtree.get( '_type' )

			if item and item_type == 'dir':
				# Папка
				if self.stdout:
					self.stdout.write( f"{current_prefix}📁 {name}/" )
				else:
					print( f"{current_prefix}📁 {name}/" )
				# Рекурсивно выводим содержимое папки
				self.print_tree( subtree, indent + 1, is_last_item, next_prefix )
			elif item and item_type == 'file':
				# Файл с размером
				try:
					file_size = item.stat().st_size
					size_str = format_size(file_size)
					if self.stdout:
						self.stdout.write( f"{current_prefix}📄 {name} ({size_str})" )
					else:
						print( f"{current_prefix}📄 {name} ({size_str})" )
				except OSError:
					if self.stdout:
						self.stdout.write( f"{current_prefix}📄 {name}" )
					else:
						print( f"{current_prefix}📄 {name}" )
			else:
				# Промежуточная папка (ещё не обработанная)
				if self.stdout:
					self.stdout.write( f"{current_prefix}📁 {name}/" )
				else:
					print( f"{current_prefix}📁 {name}/" )
				self.print_tree( subtree, indent + 1, is_last_item, next_prefix )

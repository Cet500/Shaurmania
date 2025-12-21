from django.core.exceptions import ValidationError

from Shaurmania.settings import BASE_DIR


STOP_WORDS = None


def load_stop_words():
	global STOP_WORDS

	if STOP_WORDS is None:
		stop_file = BASE_DIR / 'lists' / 'stop_words.txt'

		if stop_file.exists():
			try:
				with open(stop_file, 'r', encoding='utf-8') as f:
					STOP_WORDS = {line.strip().lower() for line in f if line.strip()}

			except UnicodeDecodeError:
				with open(stop_file, 'r', encoding='cp1251') as f:
					STOP_WORDS = {line.strip().lower() for line in f if line.strip()}

		else:
			STOP_WORDS = set()

	return STOP_WORDS


def validate_not_in_stop_words(value: str):
	"""
	Валидатор для проверки отсутствия стоп-слов в значении.
	
	Args:
		value: Строка для проверки
		
	Raises:
		ValidationError: Если найдено стоп-слово
	"""
	if not value:
		return
	
	stop_words = load_stop_words()
	
	# Проверяем полное значение
	if value.lower().strip() in stop_words:
		raise ValidationError('Это значение недоступно. Выберите другое.')

	# Проверяем отдельные слова
	words = value.split()
	for word in words:
		# Убираем знаки препинания для проверки
		clean_word = word.lower().strip('.,!?;:()[]{}"\'-')
		if clean_word and clean_word in stop_words:
			raise ValidationError('Обнаружено недопустимое слово. Выражайтесь культурнее.')

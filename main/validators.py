from django.core.exceptions import ValidationError
from Shaurmania.settings import BASE_DIR

import re


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
				# Если UTF-8 не сработал, пробуем другие кодировки
				with open(stop_file, 'r', encoding='cp1251') as f:
					STOP_WORDS = {line.strip().lower() for line in f if line.strip()}

		else:
			STOP_WORDS = set()

	return STOP_WORDS


def validate_not_in_stop_words(value: str):
	stop_words = load_stop_words()

	if value and value.lower() in stop_words:
		raise ValidationError('Это значение недоступно. Выберите другое.')

	words = value.split()

	for word in words:
		if word.lower() in stop_words:
			raise ValidationError('Обнаружение недопустимое слово. Выражайтесь культурнее.')


SOCIAL_PATTERNS = {
	'TG': re.compile( r'^https?://t\.me/[A-Za-z0-9_]{3,}$'                                         ),
	'TT': re.compile( r'^https?://(www\.)?tiktok\.com/@[A-Za-z0-9_.]{3,}/?$'                       ),
	'FB': re.compile( r'^https?://(www\.)?facebook\.com/[A-Za-z0-9_.]{3,}/?$'                      ),
	'GH': re.compile( r'^https?://(www\.)?github\.com/[A-Za-z0-9_-]{3,}/?$'                        ),
	'IG': re.compile( r'^https?://(www\.)?instagram\.com/[A-Za-z0-9_.]{3,}/?$'                     ),
	'LN': re.compile( r'^https?://(www\.)?linkedin\.com/(in|company)/[A-Za-z0-9_-]{3,}/?$'         ),
	'OK': re.compile( r'^https?://(www\.)?ok\.ru/[A-Za-z0-9_\./]{3,}$'                             ),
	'PT': re.compile( r'^https?://(www\.)?pinterest\.(com|ru)/[A-Za-z0-9_-]{3,}/?$'                ),
	'RD': re.compile( r'^https?://(www\.)?reddit\.com/user/[A-Za-z0-9_-]{3,}/?$'                   ),
	'SC': re.compile( r'^https?://(www\.)?snapchat\.com/add/[A-Za-z0-9_.]{3,}/?$'                  ),
	'TW': re.compile( r'^https?://(www\.)?(twitter|x)\.com/[A-Za-z0-9_]{3,}/?$'                    ),
	'VK': re.compile( r'^https?://(vk\.com|m\.vk\.com)/[A-Za-z0-9_\.]{3,}$'                        ),
	'WA': re.compile( r'^https?://wa\.me/[0-9]{7,15}$'                                             ),
	'YT': re.compile( r'^https?://(www\.)?youtube\.com/(@|c/|channel/|user/)?[A-Za-z0-9_-]{3,}/?$' )
}

def validate_social_link(network: str, link: str):
	pattern = SOCIAL_PATTERNS.get(network)

	if pattern and not pattern.match(link):
		raise ValidationError('Ссылка не похожа на профиль в выбранной соцсети.')

	return True

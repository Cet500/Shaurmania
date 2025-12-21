import re

from django.core.exceptions import ValidationError


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
	"""
	Валидатор для проверки соответствия ссылки формату выбранной социальной сети.
	
	Args:
		network: Код социальной сети (например, 'TG', 'FB', 'VK')
		link: URL ссылка для проверки
		
	Raises:
		ValidationError: Если ссылка не соответствует формату сети
		
	Returns:
		True: Если ссылка валидна
	"""
	if not network:
		raise ValidationError('Не указана социальная сеть.')
	
	if not link:
		raise ValidationError('Не указана ссылка.')
	
	pattern = SOCIAL_PATTERNS.get(network)
	
	if not pattern:
		raise ValidationError(f'Неподдерживаемая социальная сеть: {network}.')
	
	if not pattern.match(link):
		raise ValidationError('Ссылка не похожа на профиль в выбранной соцсети.')

	return True

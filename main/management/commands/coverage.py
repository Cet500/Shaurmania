import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command( BaseCommand ):
	help = "Запуск тестов с coverage: erase -> run -> html"

	def handle( self, *args, **options ):
		base_dir = Path( settings.BASE_DIR )

		commands = [
			['coverage', 'erase'],
			['coverage', 'run', 'manage.py', 'test'],
			['coverage', 'html'],
		]

		for cmd in commands:
			self.stdout.write( self.style.NOTICE( f"Выполняю: {' '.join( cmd )}" ) )
			proc = subprocess.run( cmd, cwd = base_dir )

			if proc.returncode != 0:
				self.stderr.write( self.style.ERROR( f"Команда завершилась с кодом {proc.returncode}: {' '.join( cmd )}" ) )
				return proc.returncode

		self.stdout.write( self.style.SUCCESS( 'Готово. Отчёт: coverage_html/index.html' ) )
		return 0



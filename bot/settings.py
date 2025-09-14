
import environ

from pathlib import Path
from os import path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env( path.join( BASE_DIR, '.env' ) )

TELEGRAM_BOT_TOKEN = env("TELEGRAM_BOT_TOKEN")
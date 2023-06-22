from .base import *

DATABASES = {"default": env.db("DATABASE_URL", default="")}

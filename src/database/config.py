import os
import re
import ssl
# {"default": "postgres://blogger:mypass@127.0.0.1:5432/blog_db"}
# "default": os.environ.get('DATABASE_URL')
config = re.match("postgres://(.*?):(.*?)@(.*?)/(.*)", os.environ.get("DATABASE_URL"))
DB_USER, DB_PASS, DB_HOST, DB = config.groups()

context = ssl.create_default_context(cafile="src/database/rds-combined-ca-bundle.pem")
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": DB,
                "host": DB_HOST.split(":")[0],
                "password": DB_PASS,
                "port": int(DB_HOST.split(":")[1]),
                "user": DB_USER,
                "ssl": context,  # Here we pass in the SSL context
            },
        }
    },
    "apps": {
        "models": {
            "models": ["src.models.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}

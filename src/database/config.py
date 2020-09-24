import os

DATABASE_URL = os.environ.get('DATABASE_URL')

# {"default": "postgres://blogger:mypass@127.0.0.1:5432/blog_db"}

TORTOISE_ORM = {
  "connections": {"default": DATABASE_URL},
  "apps": {
    "models": {
      "models": [
        "src.models.models", "aerich.models"
      ],
      "default_connection": "default"
    }
  }
}

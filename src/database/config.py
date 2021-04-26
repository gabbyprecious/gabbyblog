import os
# {"default": "postgres://blogger:mypass@127.0.0.1:5432/blog_db"}
# "default": os.environ.get('DATABASE_URL')
DATABASE_URL = os.environ.get('DATABASE_URL') + "?ssl=True"

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

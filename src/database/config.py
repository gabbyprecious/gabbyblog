import os
# {"default": "postgres://blogger:mypass@127.0.0.1:5432/blog_db"}

TORTOISE_ORM = {
  "connections": {"default": os.environ.get('DATABASE_URL')
},
  "apps": {
    "models": {
      "models": [
        "src.models.models", "aerich.models"
      ],
      "default_connection": "default"
    }
  }
}

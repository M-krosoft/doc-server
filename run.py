import os

from app.app import create_app
from app.app_config import DevelopmentSqliteConfig

config = DevelopmentSqliteConfig()
app = create_app(config=config)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port)

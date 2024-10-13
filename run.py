import os

from dotenv import load_dotenv

from app import create_app
from app.app_config import create_config

load_dotenv()

config_mode = os.getenv('CONFIG_MODE')
config = create_config(config_mode)
app = create_app(config=config)

if __name__ == '__main__':
    port = int(config.PORT)
    app.run(host="0.0.0.0", port=port)
